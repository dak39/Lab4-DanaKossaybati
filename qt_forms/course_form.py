"""
This module provides the UI for adding a new course in a PyQt5 application.

It includes a form for entering course details and handles the creation
of course records, which are managed in-memory.
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
)
from course import Course
from validators import require, validate_unique_id

def build_course_tab(parent, courses, refresh_cb):
    """
    Builds the 'Add Course' tab for the PyQt5 UI.

    This tab contains input fields for a course's ID and name, and a button
    to add the new course to the in-memory list.

    :param parent: The parent widget.
    :type parent: QWidget
    :param courses: The list of course objects.
    :type courses: list[Course]
    :param refresh_cb: A callback function to refresh the main application's data view.
    :type refresh_cb: callable
    :return: The group box containing the course creation UI.
    :rtype: QGroupBox
    """
    frame = QGroupBox("Add Course", parent)

    layout = QGridLayout(frame)
    layout.setContentsMargins(10, 10, 10, 10)

    # Labls
    tk_label_id = QLabel("Course ID:", frame)
    layout.addWidget(tk_label_id, 0, 0)
    tk_label_name = QLabel("Course Name:", frame)
    layout.addWidget(tk_label_name, 1, 0)

    id_input   = QLineEdit(frame)
    name_input = QLineEdit(frame)

    layout.addWidget(id_input,   0, 1)
    layout.addWidget(name_input, 1, 1)

    def add_course():
        """
        Handles the logic for adding a new course. It retrieves user input,
        validates it, creates a Course object, and adds it to the list.
        """
        course_id   = id_input.text().strip()
        course_name = name_input.text().strip()

        if not (require(course_id, "Course ID") and require(course_name, "Course Name")):
            return

        if not validate_unique_id(course_id, courses, "course_id"):
            return

        course = Course(course_id=course_id, course_name=course_name)
        courses.append(course)
        QMessageBox.information(frame, "Success", "Course Added!")
        id_input.clear()
        name_input.clear()
        refresh_cb()

    add_button = QPushButton("Add Course", frame)
    add_button.clicked.connect(add_course)
    layout.addWidget(add_button, 2, 1,  alignment=Qt.AlignRight)

    return frame
