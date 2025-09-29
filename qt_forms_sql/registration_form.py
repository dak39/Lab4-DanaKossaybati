"""
This module provides a function to build the 'Student Registration' tab for the PyQt5-based GUI.

It allows registering a student for a course, with data being persisted via a database manager.
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox, QLabel, QComboBox, QPushButton, QMessageBox, QGridLayout
)


def build_registration_tab(parent, db_manager, refresh_cb):
    """
    Builds the 'Student Registration' tab for the PyQt5 application.

    This function creates a QGroupBox for registering a student in a course.
    It includes dropdowns for selecting a student and a course, and a 'Register' button.
    The data is fetched from and saved to the database via the provided db_manager.

    :param parent: The parent widget for this tab.
    :type parent: QtWidgets.QWidget
    :param db_manager: The database manager instance for database operations.
    :type db_manager: DatabaseManager
    :param refresh_cb: A callback function to refresh other parts of the UI after a registration.
    :type refresh_cb: function
    :return: A QGroupBox widget containing the registration form.
    :rtype: QGroupBox
    """
    frame = QGroupBox("Student Registration", parent)

    layout = QGridLayout(frame)
    layout.setContentsMargins(10, 10, 10, 10)

    layout.addWidget(QLabel("Student:", frame), 0, 0)
    layout.addWidget(QLabel("Course:", frame), 1, 0)

    student_box = QComboBox(frame)
    student_box.setEditable(False) 
    student_box.setMinimumContentsLength(40)
    layout.addWidget(student_box, 0, 1)

    course_box = QComboBox(frame)
    course_box.setEditable(False)
    course_box.setMinimumContentsLength(40)
    layout.addWidget(course_box, 1, 1)

    def refresh_boxes():
        """
        Refreshes the contents of the student and course dropdown boxes.

        Fetches the latest lists of students and courses from the database
        and populates the dropdowns.
        """
        students = db_manager.get_all_students()
        courses = db_manager.get_all_courses()

        student_box.blockSignals(True)
        course_box.blockSignals(True)

        student_box.clear()
        student_box.addItems([student.display_student() for student in students])

        course_box.clear()
        course_box.addItems([course.display_course() for course in courses])

        student_box.setCurrentIndex(-1)
        course_box.setCurrentIndex(-1)

        student_box.blockSignals(False)
        course_box.blockSignals(False)

        # Store the current lists for later reference
        frame.current_students = students
        frame.current_courses = courses

    def register_student():
        """
        Handles the 'Register' button click event.

        Registers the selected student for the selected course and saves the
        registration to the database. Shows a success or error message.
        """
        student_index = student_box.currentIndex()
        course_index = course_box.currentIndex()

        if student_index == -1 or course_index == -1:
            QMessageBox.warning(frame, "Select both", "Please select a student and a course.")
            return

        selected_student = frame.current_students[student_index]
        selected_course = frame.current_courses[course_index]

        try:
            db_manager.register_student_course(selected_student.student_id, selected_course.course_id)
            QMessageBox.information(
                frame, "Success",
                f"Registered {selected_student.name} to {selected_course.course_id} - {selected_course.course_name}"
            )
            refresh_cb()
            refresh_boxes()
        except ValueError as e:
            QMessageBox.warning(frame, "Error", str(e))

    register_button = QPushButton("Register", frame)
    register_button.clicked.connect(register_student)
    layout.addWidget(register_button, 2, 1, alignment=Qt.AlignRight)

    # Initial load of the boxes
    refresh_boxes()
    
    frame.refresh_boxes = refresh_boxes
    return frame