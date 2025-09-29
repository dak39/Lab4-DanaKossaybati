"""
This module serves as the main entry point for the PyQt5-based School Management System,
which uses an SQLite database for data persistence.

It sets up the main application window, initializes the database manager, and builds the
tabbed user interface for managing students, instructors, courses, registrations, and assignments.
"""
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
)

from qt_forms_sql.student_form import build_student_tab
from qt_forms_sql.instructor_form import build_instructor_tab
from qt_forms_sql.course_form import build_course_tab
from qt_forms_sql.registration_form import build_registration_tab
from qt_forms_sql.assignment_form import build_assignment_tab
from qt_forms_sql.records_form import build_records_tab

from database_manager import DatabaseManager

class MainWindow(QMainWindow):
    """
    The main window of the application, which contains the tabbed interface.

    :param title: The title of the main window.
    :type title: str
    """
    def __init__(self, title="School Management System - SQLite"):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(800, 600)

        # Initialize database manager
        self.db_manager = DatabaseManager()

        # Build the UI
        self.build_ui()

    def build_ui(self):
        """
        Constructs the user interface, including the tab control and all the individual tabs.
        """
        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create tab widget
        tab_control = QTabWidget(central_widget)
        layout.addWidget(tab_control)

        # Create tabs
        student_tab = QWidget()
        instructor_tab = QWidget()
        course_tab = QWidget()
        registration_tab = QWidget()
        assignment_tab = QWidget()
        records_tab = QWidget()

        # Add tabs to control
        tab_control.addTab(student_tab, "Students")
        tab_control.addTab(instructor_tab, "Instructors")
        tab_control.addTab(course_tab, "Courses")
        tab_control.addTab(registration_tab, "Registration")
        tab_control.addTab(assignment_tab, "Assignment")
        tab_control.addTab(records_tab, "Records")

        # Build each tab
        def refresh_all():
            """
            Refreshes the data in all relevant tabs to ensure the UI is up-to-date.
            """
            try:
                if registration_frame and hasattr(registration_frame, 'refresh_boxes'):
                    registration_frame.refresh_boxes()
                if assignment_frame and hasattr(assignment_frame, 'refresh_boxes'):
                    assignment_frame.refresh_boxes()
                if hasattr(self, 'records_frame') and hasattr(self.records_frame, 'refresh_records'):
                    self.records_frame.refresh_records()
            except Exception as e:
                print(f"Error in refresh_all: {str(e)}")

        # Create each tab's content with layouts
        student_layout = QVBoxLayout(student_tab)
        student_layout.addWidget(build_student_tab(student_tab, self.db_manager, refresh_all))

        instructor_layout = QVBoxLayout(instructor_tab)
        instructor_layout.addWidget(build_instructor_tab(instructor_tab, self.db_manager, refresh_all))

        course_layout = QVBoxLayout(course_tab)
        course_layout.addWidget(build_course_tab(course_tab, self.db_manager, refresh_all))

        registration_layout = QVBoxLayout(registration_tab)
        registration_frame = build_registration_tab(registration_tab, self.db_manager, refresh_all)
        registration_layout.addWidget(registration_frame)

        assignment_layout = QVBoxLayout(assignment_tab)
        assignment_frame = build_assignment_tab(assignment_tab, self.db_manager, refresh_all)
        assignment_layout.addWidget(assignment_frame)

        records_layout = QVBoxLayout(records_tab)
        records_frame = build_records_tab(records_tab, self.db_manager)
        records_layout.addWidget(records_frame)
        self.records_frame = records_frame  # Store reference to records frame

        # Initial load of all data
        refresh_all()

def main():
    """
    The main function to run the PyQt5 application.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
