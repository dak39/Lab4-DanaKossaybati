"""
This module provides the UI for assigning instructors to courses in a PyQt5 application.

It allows selecting an instructor and a course from dropdowns and assigning
the former to the latter, with data managed in-memory.
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox, QLabel, QComboBox, QPushButton, QMessageBox, QGridLayout
)

def clear_dropdowns(instructor_box, course_box):
    """
    Clears the current selection in the instructor and course comboboxes.

    :param instructor_box: The instructor combobox widget.
    :type instructor_box: QComboBox
    :param course_box: The course combobox widget.
    :type course_box: QComboBox
    """
    try:
        instructor_box.setCurrentIndex(-1)
        instructor_box.setCurrentText("")
        course_box.setCurrentIndex(-1)
        course_box.setCurrentText("")
    except Exception:
        pass

def build_assignment_tab(parent, instructors, courses, refresh_cb):
    """
    Builds the 'Instructor Assignment' tab for the PyQt5 UI.

    This tab allows users to assign an instructor to a course.

    :param parent: The parent widget.
    :type parent: QWidget
    :param instructors: A list of all instructor objects.
    :type instructors: list[Instructor]
    :param courses: A list of all course objects.
    :type courses: list[Course]
    :param refresh_cb: A callback function to refresh the main application's data view.
    :type refresh_cb: callable
    :return: The group box containing the assignment UI. It includes a 'refresh_boxes'
             method to allow external updates to the dropdowns.
    :rtype: QGroupBox
    """
    frame = QGroupBox("Instructor Assignment", parent)

    layout = QGridLayout(frame)
    layout.setContentsMargins(10, 10, 10, 10)

    # Labels
    tk_label_instructor = QLabel("Instructor:", frame)
    layout.addWidget(tk_label_instructor, 0, 0)
    tk_label_course = QLabel("Course:", frame)
    layout.addWidget(tk_label_course, 1, 0)


    instructor_box  = QComboBox(frame)
    instructor_box.setEditable(False)  
    instructor_box.setMinimumContentsLength(40)
    instructor_box.addItems([instructor.display_instructor() for instructor in instructors])
    layout.addWidget(instructor_box, 0, 1)

    course_box = QComboBox(frame)
    course_box.setEditable(False)
    course_box.setMinimumContentsLength(40)
    course_box.addItems([course.display_course() for course in courses])
    layout.addWidget(course_box, 1, 1)

    def refresh_boxes():
        """
        Refreshes the items in the instructor and course comboboxes.
        """
        instructor_box.blockSignals(True)
        course_box.blockSignals(True)

        instructor_box.clear()
        instructor_box.addItems([instructor.display_instructor() for instructor in instructors])

        course_box.clear()
        course_box.addItems([course.display_course() for course in courses])


        # clear
        instructor_box.setCurrentIndex(-1)
        course_box.setCurrentIndex(-1)

        instructor_box.blockSignals(False)
        course_box.blockSignals(False)
        
    def assign_instructor():
        """
        Handles the logic for assigning an instructor to a course.
        """
        instructor_index = instructor_box.currentIndex()
        course_index = course_box.currentIndex()
        
        if instructor_index == -1 or course_index == -1:
            QMessageBox.warning(frame, "Select both", "Please select an instructor and a course.")
            return
        
        selected_instructor = instructors[instructor_index]
        selected_course = courses[course_index]

        if selected_course.instructor and selected_course.instructor.instructor_id == selected_instructor.instructor_id:
            QMessageBox.information(frame, "Already assigned",
                                    f"{selected_instructor.name} is already assigned to {selected_course.course_name}.")
            return

        if selected_course.instructor and selected_course.instructor.instructor_id != selected_instructor.instructor_id:
            reply = QMessageBox.question(
                frame, "Replace instructor",
                f"{selected_course.course_name} already has {selected_course.instructor.name}. Replace?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return

        selected_instructor.assign_course(selected_course)
        selected_course.add_instructor(selected_instructor)

        QMessageBox.information(
            frame, "Success",
            f"Assigned {selected_instructor.name} to {selected_course.course_name} - {selected_course.course_name}"
        )
        refresh_cb()
        instructor_box.setCurrentIndex(-1)
        course_box.setCurrentIndex(-1)
        clear_dropdowns(instructor_box, course_box)

    assign_button = QPushButton("Assign", frame)
    assign_button.clicked.connect(assign_instructor)
    layout.addWidget(assign_button, 2, 1, alignment=Qt.AlignRight)

    frame.refresh_boxes = refresh_boxes
    return frame
