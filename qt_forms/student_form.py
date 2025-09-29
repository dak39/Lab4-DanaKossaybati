"""
This module provides a function to build the 'Add Student' tab for the PyQt5-based GUI.

It includes a form for adding a new student with fields for name, age, email, and student ID.
Input validation is performed before adding the student to the data source.
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox, QLabel, QLineEdit, QPushButton, QMessageBox,
    QGridLayout
)

from student import Student
from validators import validate_name, validate_age, require, validate_email, validate_unique_id


def build_student_tab(parent: QtWidgets.QWidget, students: list, refresh_cb):
    """
    Builds the 'Add Student' tab for the PyQt5 application.

    This function creates a QGroupBox containing a form to add a new student.
    The form includes input fields for the student's name, age, email, and student ID.
    An 'Add Student' button triggers the validation and addition of the student.

    :param parent: The parent widget for this tab.
    :type parent: QtWidgets.QWidget
    :param students: A list of existing Student objects to ensure the new student ID is unique.
    :type students: list
    :param refresh_cb: A callback function to be called after a student is successfully added,
                       to refresh the display of student records.
    :type refresh_cb: function
    :return: A QGroupBox widget containing the student form.
    :rtype: QGroupBox
    """
    frame = QGroupBox("Add Student", parent)

    layout = QGridLayout(frame)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setHorizontalSpacing(8)
    layout.setVerticalSpacing(8)

    # Labels
    layout.addWidget(QLabel("Name:"),      0, 0)
    layout.addWidget(QLabel("Age:"),       1, 0)
    layout.addWidget(QLabel("Email:"),     2, 0)
    layout.addWidget(QLabel("Student ID:"),3, 0)

    # Inputs
    name_input  = QLineEdit(frame)
    age_input   = QLineEdit(frame)
    email_input = QLineEdit(frame)
    id_input    = QLineEdit(frame)

    layout.addWidget(name_input,  0, 1)
    layout.addWidget(age_input,   1, 1)
    layout.addWidget(email_input, 2, 1)
    layout.addWidget(id_input,    3, 1)

    # Button
    add_button = QPushButton("Add Student", frame)
    layout.addWidget(add_button, 4, 1, alignment=Qt.AlignRight)

    def add_student():
        """
        Handles the 'Add Student' button click event.

        Retrieves user input, validates it, creates a new Student object,
        and adds it to the list of students. Shows a success message
        and clears the input fields. Finally, it calls the refresh callback.
        """
        name  = name_input.text().strip()
        age   = age_input.text().strip()
        email = email_input.text().strip()
        sid   = id_input.text().strip()

        # validate inputs (same flow as Tkinter)
        if not (validate_name(name) and validate_age(age) and validate_email(email) and require(sid, "Student ID")):
            return

        # unique ID check
        if not validate_unique_id(sid, students, "student_id"):
            return

        student = Student(name=name, age=age, email=email, student_id=sid)
        students.append(student)

        QMessageBox.information(frame, "Success", "Student Added!")

        name_input.clear()
        age_input.clear()
        email_input.clear()
        id_input.clear()

        refresh_cb()

    add_button.clicked.connect(add_student)

    return frame
