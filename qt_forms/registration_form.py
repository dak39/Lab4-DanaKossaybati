"""
This module provides the UI for registering students into courses in a PyQt5 application.

It allows selecting a student and a course from dropdowns and registering the student
for the course, with data managed in-memory.
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox, QLabel, QComboBox, QPushButton, QMessageBox, QGridLayout
)

def build_registration_tab(parent, students, courses, refresh_cb):
    """
    Builds the 'Student Registration' tab for the PyQt5 UI.

    :param parent: The parent widget.
    :type parent: QWidget
    :param students: The list of student objects.
    :type students: list[Student]
    :param courses: The list of course objects.
    :type courses: list[Course]
    :param refresh_cb: A callback function to refresh the main application's data view.
    :type refresh_cb: callable
    :return: The group box containing the registration UI. It includes a 'refresh_boxes'
             method to allow external updates to the dropdowns.
    :rtype: QGroupBox
    """
    frame = QGroupBox("Student Registration", parent)

    layout = QGridLayout(frame)
    layout.setContentsMargins(10, 10, 10, 10)

    tk_Label_student = QLabel("Student:", frame)
    tk_Label_course  = QLabel("Course:", frame)
    layout.addWidget(tk_Label_student, 0, 0)
    layout.addWidget(tk_Label_course,  1, 0)


    student_box = QComboBox(frame)
    student_box.setEditable(False) 
    student_box.setMinimumContentsLength(40)
    student_box.addItems([s.display_student() for s in students])
    layout.addWidget(student_box, 0, 1)

    course_box = QComboBox(frame)
    course_box.setEditable(False)
    course_box.setMinimumContentsLength(40)
    course_box.addItems([c.display_course() for c in courses])
    layout.addWidget(course_box, 1, 1)

    def refresh_boxes():
        """
        Refreshes the items in the student and course comboboxes.
        """
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

    # registration logc
    def register_student():
        """
        Handles the logic for registering a student in a course.
        """
        student_index = student_box.currentIndex()
        course_index  = course_box.currentIndex()

        if student_index == -1 or course_index == -1:
            QMessageBox.warning(frame, "Select both", "Please select a student and a course.")
            return

        selected_student = students[student_index]
        selected_course  = courses[course_index]

        # prevent duplicates
        if any(registered_course == selected_course.course_id
               for registered_course in getattr(selected_student, "registered_courses", [])):
            QMessageBox.information(frame, "Already registered",
                                    f"{selected_student.name} is already in {selected_course.course_id}.")
            return

        selected_student.register_course(selected_course)
        selected_course.add_student(selected_student)

        QMessageBox.information(
            frame, "Success",
            f"Registered {selected_student.name} to {selected_course.course_id} - {selected_course.course_name}"
        )

        refresh_cb()
        refresh_boxes()

    # here we add the functionality of registering a coutrse to the button
    register_button = QPushButton("Register", frame)
    register_button.clicked.connect(register_student)
    layout.addWidget(register_button, 2, 1, alignment=Qt.AlignRight)

    frame.refresh_boxes = refresh_boxes
    student_box.setCurrentIndex(-1)
    course_box.setCurrentIndex(-1)

    return frame
