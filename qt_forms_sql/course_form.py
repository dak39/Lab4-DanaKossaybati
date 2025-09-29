"""
This module provides a function to build the 'Add Course' tab for the PyQt5-based GUI.

It includes a form for adding a new course with fields for course ID and name.
Input validation is performed, and the new course is persisted to the database.
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
)
from course import Course
from validators import require

def build_course_tab(parent, db_manager, refresh_cb):
    """
    Builds the 'Add Course' tab for the PyQt5 application.

    This function creates a QGroupBox containing a form to add a new course.
    The form includes input fields for the course ID and course name.
    An 'Add Course' button triggers validation and saves the course to the database.

    :param parent: The parent widget for this tab.
    :type parent: QtWidgets.QWidget
    :param db_manager: The database manager instance for database operations.
    :type db_manager: DatabaseManager
    :param refresh_cb: A callback function to be called after a course is successfully added,
                       to refresh the display of course records.
    :type refresh_cb: function
    :return: A QGroupBox widget containing the course form.
    :rtype: QGroupBox
    """
    frame = QGroupBox("Add Course", parent)

    layout = QGridLayout(frame)
    layout.setContentsMargins(10, 10, 10, 10)

    # Labels
    layout.addWidget(QLabel("Course ID:", frame), 0, 0)
    layout.addWidget(QLabel("Course Name:", frame), 1, 0)

    id_input = QLineEdit(frame)
    name_input = QLineEdit(frame)

    layout.addWidget(id_input, 0, 1)
    layout.addWidget(name_input, 1, 1)

    def add_course():
        """
        Handles the 'Add Course' button click event.

        Retrieves user input, validates it, creates a new Course object,
        and adds it to the database. Shows a success or error message
        and clears the input fields. Finally, it calls the refresh callback.
        """
        course_id = id_input.text().strip()
        course_name = name_input.text().strip()

        if not (require(course_id, "Course ID") and
                require(course_name, "Course Name")):
            return


        try:
            course = Course(course_id=course_id, course_name=course_name)
            db_manager.add_course(course)
            QMessageBox.information(frame, "Success", "Course Added!")
            id_input.clear()
            name_input.clear()

            refresh_cb()
        except ValueError as e:
            QMessageBox.warning(frame, "Error", str(e))

    add_button = QPushButton("Add Course", frame)
    add_button.clicked.connect(add_course)
    layout.addWidget(add_button, 3, 1, alignment=Qt.AlignRight)

    return frame