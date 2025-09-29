"""
This module provides a function to build the 'Instructor Assignment' tab for the PyQt5-based GUI.

It allows assigning an instructor to a course, with data being persisted via a database manager.
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox, QLabel, QComboBox, QPushButton, QMessageBox, QGridLayout
)

def build_assignment_tab(parent, db_manager, refresh_cb):
    """
    Builds the 'Instructor Assignment' tab for the PyQt5 application.

    This function creates a QGroupBox for assigning an instructor to a course.
    It includes dropdowns for selecting an instructor and a course, and an 'Assign' button.
    The data is fetched from and saved to the database via the provided db_manager.

    :param parent: The parent widget for this tab.
    :type parent: QtWidgets.QWidget
    :param db_manager: The database manager instance for database operations.
    :type db_manager: DatabaseManager
    :param refresh_cb: A callback function to refresh other parts of the UI after an assignment.
    :type refresh_cb: function
    :return: A QGroupBox widget containing the assignment form.
    :rtype: QGroupBox
    """
    frame = QGroupBox("Instructor Assignment", parent)

    layout = QGridLayout(frame)
    layout.setContentsMargins(10, 10, 10, 10)

    # Labels
    layout.addWidget(QLabel("Instructor:", frame), 0, 0)
    layout.addWidget(QLabel("Course:", frame), 1, 0)

    instructor_box = QComboBox(frame)
    instructor_box.setEditable(False)
    instructor_box.setMinimumContentsLength(40)
    layout.addWidget(instructor_box, 0, 1)

    course_box = QComboBox(frame)
    course_box.setEditable(False)
    course_box.setMinimumContentsLength(40)
    layout.addWidget(course_box, 1, 1)

    def refresh_boxes():
        """
        Refreshes the contents of the instructor and course dropdown boxes.

        Fetches the latest lists of instructors and courses from the database
        and populates the dropdowns.
        """
        instructors = db_manager.get_all_instructors()
        courses = db_manager.get_all_courses()

        instructor_box.blockSignals(True)
        course_box.blockSignals(True)

        instructor_box.clear()
        instructor_box.addItems([instructor.display_instructor() for instructor in instructors])

        course_box.clear()
        course_box.addItems([course.display_course() for course in courses])

        instructor_box.setCurrentIndex(-1)
        course_box.setCurrentIndex(-1)

        instructor_box.blockSignals(False)
        course_box.blockSignals(False)

        # Store the current lists for later reference
        frame.current_instructors = instructors
        frame.current_courses = courses

    def assign_instructor():
        """
        Handles the 'Assign' button click event.

        Assigns the selected instructor to the selected course and saves the
        assignment to the database. Shows a success or error message.
        """
        instructor_index = instructor_box.currentIndex()
        course_index = course_box.currentIndex()

        if instructor_index == -1 or course_index == -1:
            QMessageBox.warning(frame, "Select both", "Please select an instructor and a course.")
            return

        selected_instructor = frame.current_instructors[instructor_index]
        selected_course = frame.current_courses[course_index]

        try:
            db_manager.assign_instructor_course(selected_instructor.instructor_id, selected_course.course_id)
            QMessageBox.information(
                frame, "Success",
                f"Assigned {selected_instructor.name} to {selected_course.course_name}"
            )
            refresh_cb()
            refresh_boxes()
        except ValueError as e:
            QMessageBox.warning(frame, "Error", str(e))

    assign_button = QPushButton("Assign", frame)
    assign_button.clicked.connect(assign_instructor)
    layout.addWidget(assign_button, 2, 1, alignment=Qt.AlignRight)

    # Initial load of the boxes
    refresh_boxes()

    frame.refresh_boxes = refresh_boxes
    return frame