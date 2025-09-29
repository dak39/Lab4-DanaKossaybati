"""
This module provides a function to build the 'Add Instructor' tab for the PyQt5-based GUI.

It includes a form for adding a new instructor with fields for name, age, email, and instructor ID.
Input validation is performed, and the new instructor is persisted to the database.
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
)
from instructor import Instructor
from validators import validate_name, validate_age, validate_email, require

def build_instructor_tab(parent, db_manager, refresh_cb):
    """
    Builds the 'Add Instructor' tab for the PyQt5 application.

    This function creates a QGroupBox containing a form to add a new instructor.
    The form includes input fields for the instructor's name, age, email, and ID.
    An 'Add Instructor' button triggers validation and saves the instructor to the database.

    :param parent: The parent widget for this tab.
    :type parent: QtWidgets.QWidget
    :param db_manager: The database manager instance for database operations.
    :type db_manager: DatabaseManager
    :param refresh_cb: A callback function to be called after an instructor is successfully added,
                       to refresh the display of instructor records.
    :type refresh_cb: function
    :return: A QGroupBox widget containing the instructor form.
    :rtype: QGroupBox
    """
    frame = QGroupBox("Add Instructor", parent)

    layout = QGridLayout(frame)
    layout.setContentsMargins(10, 10, 10, 10)

    layout.addWidget(QLabel("Name:", frame), 0, 0)
    layout.addWidget(QLabel("Age:", frame), 1, 0)
    layout.addWidget(QLabel("Email:", frame), 2, 0)
    layout.addWidget(QLabel("Instructor ID:", frame), 3, 0)

    name_input = QLineEdit(frame)
    age_input = QLineEdit(frame)
    email_input = QLineEdit(frame)
    id_input = QLineEdit(frame)

    layout.addWidget(name_input, 0, 1)
    layout.addWidget(age_input, 1, 1)
    layout.addWidget(email_input, 2, 1)
    layout.addWidget(id_input, 3, 1)

    def add_instructor():
        """
        Handles the 'Add Instructor' button click event.

        Retrieves user input, validates it, creates a new Instructor object,
        and adds it to the database. Shows a success or error message
        and clears the input fields. Finally, it calls the refresh callback.
        """
        name = name_input.text().strip()
        age = age_input.text().strip()
        email = email_input.text().strip()
        instructor_id = id_input.text().strip()

        # validate inputs
        if not (validate_name(name) and validate_age(age) and validate_email(email)
                and require(instructor_id, "Instructor ID") and require(name, "Name") and require(email, "Email") and require(age, "Age")):
            return

        try:
            instructor = Instructor(name=name, age=age, email=email, instructor_id=instructor_id)
            db_manager.add_instructor(instructor)
            QMessageBox.information(frame, "Success", "Instructor Added!")

            name_input.clear()
            age_input.clear()
            email_input.clear()
            id_input.clear()

            refresh_cb()
        except ValueError as e:
            QMessageBox.warning(frame, "Error", str(e))

    add_button = QPushButton("Add Instructor", frame)
    add_button.clicked.connect(add_instructor)
    layout.addWidget(add_button, 4, 1, alignment=Qt.AlignRight)

    return frame