"""
This module serves as the main entry point for the PyQt5-based School Management System,
which uses JSON files for data persistence.

It sets up the main application window and builds the tabbed user interface
for managing students, instructors, courses, registrations, and assignments.
"""
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout

from qt_forms.student_form import build_student_tab
from qt_forms.instructor_form import build_instructor_tab
from qt_forms.course_form import build_course_tab
from qt_forms.registration_form import build_registration_tab
from qt_forms.assignment_form import build_assignment_tab
from qt_forms.records_form import build_records_tab

def main():
    """
    Initializes and runs the PyQt5-based School Management System UI.

    This function sets up the main window, creates the tabbed interface,
    and connects the necessary callbacks to ensure data stays synchronized
    across the different parts of the application.
    """
    app = QApplication(sys.argv)

    root = QtWidgets.QMainWindow()
    root.setWindowTitle("School Management System")
    root.resize(1000, 720)

    central_widget = QWidget(root)
    root.setCentralWidget(central_widget)
    main_layout = QVBoxLayout(central_widget)

    # In-memory data stores
    students = []
    instructors = []
    courses = []

    tabs = QTabWidget(central_widget)
    main_layout.addWidget(tabs)

    student_tab = QWidget()
    instructor_tab = QWidget()
    course_tab = QWidget()
    registration_tab = QWidget()
    assignment_tab = QWidget()
    records_tab = QWidget()

    tabs.addTab(student_tab, "Student")
    tabs.addTab(instructor_tab, "Instructor")
    tabs.addTab(course_tab, "Courses")
    tabs.addTab(registration_tab, "Register Student")
    tabs.addTab(assignment_tab, "Assign Instructor")
    tabs.addTab(records_tab, "All Records")

    # Build records tab first as other tabs might need to refresh it
    rec_layout = QVBoxLayout(records_tab)
    tree, refresh_table, records_container = build_records_tab(
        records_tab, students, instructors, courses, on_data_change=None
    )
    rec_layout.addWidget(records_container)

    # Build registration and assignment tabs
    reg_layout = QVBoxLayout(registration_tab)
    registration_frame = build_registration_tab(
        registration_tab, students, courses, refresh_table
    )
    reg_layout.addWidget(registration_frame)

    assign_layout = QVBoxLayout(assignment_tab)
    assignment_frame = build_assignment_tab(
        assignment_tab, instructors, courses, refresh_table
    )
    assign_layout.addWidget(assignment_frame)

    def refresh_dropdowns():
        """Refreshes the contents of comboboxes in the registration and assignment tabs."""
        if hasattr(registration_frame, "refresh_boxes"):
            registration_frame.refresh_boxes()
        if hasattr(assignment_frame, "refresh_boxes"):
            assignment_frame.refresh_boxes()
        if hasattr(registration_frame, "clear_dropdowns"):
            registration_frame.clear_dropdowns()
        if hasattr(assignment_frame, "clear_dropdowns"):
            assignment_frame.clear_dropdowns()

    def refresh_all():
        """Refreshes all data views, including the main records table and dropdowns."""
        refresh_table()
        refresh_dropdowns()

    if hasattr(tree, '_on_data_change'):
        tree._on_data_change = refresh_dropdowns
    
    if hasattr(registration_frame, "refresh_cb"):
        registration_frame.refresh_cb = refresh_all
    if hasattr(assignment_frame, "refresh_cb"):
        assignment_frame.refresh_cb = refresh_all

    # Build remaining tabs
    stud_layout = QVBoxLayout(student_tab)
    stud_layout.addWidget(build_student_tab(student_tab, students, refresh_all))

    instr_layout = QVBoxLayout(instructor_tab)
    instr_layout.addWidget(build_instructor_tab(instructor_tab, instructors, refresh_all))

    course_layout = QVBoxLayout(course_tab)
    course_layout.addWidget(build_course_tab(course_tab, courses, refresh_all))

    # Initial data load
    refresh_all()

    root.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
