"""
This module provides the UI for adding a new course in a Tkinter application.
"""

import tkinter as tk
from tkinter import messagebox
from course import Course
from validators import require, validate_unique_id

def build_course_tab(parent, courses, refresh_cb):
    """
    Builds the course creation tab for the Tkinter UI.

    :param parent: The parent widget.
    :type parent: tk.Widget
    :param courses: A list of all course objects.
    :type courses: list[Course]
    :param refresh_cb: A callback function to refresh the main application's data.
    :type refresh_cb: callable
    :return: The frame containing the course creation tab's UI.
    :rtype: tk.LabelFrame
    """
    
    frame = tk.LabelFrame(parent, text="Add Course", padx=10, pady=10)
    frame.pack(padx=20, pady=20, fill="x")

    tk.Label(frame, text="Course ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    id_input   = tk.Entry(frame)
    id_input.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame, text="Course Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    name_input = tk.Entry(frame)
    name_input.grid(row=1, column=1, padx=5, pady=5)

    def add_course():
        """
        Handles the logic for adding a new course.
        """
        course_id = id_input.get().strip()
        course_name = name_input.get().strip()
        
        # make sure that the user filed the required fields
        if not (require(course_id, "Course ID") and require(course_name, "Course Name")):
            return
        
        if not validate_unique_id(course_id, courses, "course_id"):
            return

        course = Course(course_id=course_id, course_name=course_name)
        courses.append(course)
        messagebox.showinfo("Success", "Course Added!")
        id_input.delete(0, tk.END)
        name_input.delete(0, tk.END)
        refresh_cb()

    tk.Button(frame, text="Add Course", command=add_course).grid(row=2, column=1, pady=10, sticky="e")
    return frame
