"""
This module provides the UI for adding a new instructor in a PyQt5 application.

It includes a form for entering instructor details and handles the creation
of instructor records, which are managed in-memory.
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
)
from instructor import Instructor
from validators import validate_name, validate_age, validate_email, require, validate_unique_id

def build_instructor_tab(parent, instructors, refresh_cb):
    """
    Builds the 'Add Instructor' tab for the PyQt5 UI.

    This tab contains input fields for an instructor's details (name, age, email, ID)
    and a button to add the new instructor to the in-memory list.

    :param parent: The parent widget.
    :type parent: QWidget
    :param instructors: The list of instructor objects.
    :type instructors: list[Instructor]
    :param refresh_cb: A callback function to refresh the main application's data view.
    :type refresh_cb: callable
    :return: The group box containing the instructor creation UI.
    :rtype: QGroupBox
    """
    frame = QGroupBox("Add Instructor", parent)

    layout = QGridLayout(frame)
    layout.setContentsMargins(10, 10, 10, 10)

    QLabel("Name:").setParent(frame)
    tk_label_name = QLabel("Name:", frame)
    layout.addWidget(tk_label_name, 0, 0)

    tk_label_age = QLabel("Age:", frame)
    layout.addWidget(tk_label_age, 1, 0)

    tk_label_email = QLabel("Email:", frame)
    layout.addWidget(tk_label_email, 2, 0)

    tk_label_id = QLabel("Instructor ID:", frame)
    layout.addWidget(tk_label_id, 3, 0)

    # keep variable names identical
    name_input  = QLineEdit(frame)
    age_input   = QLineEdit(frame)
    email_input = QLineEdit(frame)
    id_input    = QLineEdit(frame)

    layout.addWidget(name_input,  0, 1)
    layout.addWidget(age_input,   1, 1)
    layout.addWidget(email_input, 2, 1)
    layout.addWidget(id_input,    3, 1)

    def add_instructor():
        """
        Handles the logic for adding a new instructor. It retrieves user input,
        validates it, creates an Instructor object, and adds it to the list.
        """
        name  = name_input.text().strip()
        age   = age_input.text().strip()
        email = email_input.text().strip()
        iid   = id_input.text().strip()

        # validate inpts
        if not (validate_name(name) and validate_age(age) and validate_email(email) and require(iid, "Instructor ID")):
            return

        # check unique ID
        if not validate_unique_id(iid, instructors, "instructor_id"):
            return

        instructor = Instructor(name=name, age=age, email=email, instructor_id=iid)
        instructors.append(instructor)
        QMessageBox.information(frame, "Success", "Instructor Added!")

        name_input.clear()
        age_input.clear()
        email_input.clear()
        id_input.clear()

        refresh_cb()

    add_button = QPushButton("Add Instructor", frame)
    add_button.clicked.connect(add_instructor)
    layout.addWidget(add_button, 4, 1, alignment=Qt.AlignRight)

    return frame
