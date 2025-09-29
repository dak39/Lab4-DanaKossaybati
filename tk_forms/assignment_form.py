"""
This module provides the UI for assigning an instructor to a course in a Tkinter application.
"""

import tkinter as tk
from tkinter import ttk, messagebox

def clear_dropdowns(instructor_box, course_box):
    """
    Clears the selection in the instructor and course dropdowns.

    :param instructor_box: The combobox for instructors.
    :type instructor_box: ttk.Combobox
    :param course_box: The combobox for courses.
    :type course_box: ttk.Combobox
    """
    instructor_box.set("")
    course_box.set("")

def build_assignment_tab(parent, instructors, courses, refresh_cb):
    """
    Builds the instructor assignment tab for the Tkinter UI.

    :param parent: The parent widget.
    :type parent: tk.Widget
    :param instructors: A list of all instructor objects.
    :type instructors: list[Instructor]
    :param courses: A list of all course objects.
    :type courses: list[Course]
    :param refresh_cb: A callback function to refresh the main application's data.
    :type refresh_cb: callable
    :return: The frame containing the assignment tab's UI.
    :rtype: tk.LabelFrame
    """
    
    frame = tk.LabelFrame(parent, text="Instructor Assignment", padx=10, pady=10)
    frame.pack(padx=20, pady=20, fill="x")

    tk.Label(frame, text="Instructor:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    instructor_box  = ttk.Combobox(frame, state="readonly", width=40, values=[i.display_instructor() for i in instructors])
    instructor_box.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame, text="Course:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    course_box = ttk.Combobox(frame, state="readonly", width=40, values=[c.display_course() for c in courses])
    course_box.grid(row=1, column=1, padx=5, pady=5)

    def refresh_boxes():
        """
        Refreshes the values in the instructor and course dropdowns.
        """
        instructor_box["values"]  = [i.display_instructor() for i in instructors]
        course_box["values"] = [c.display_course() for c in courses]
        
        
    def assign_instructor():
        """
        Handles the logic for assigning an instructor to a course.
        """
        instructor_index = instructor_box.current()
        course_index = course_box.current()
        
        if instructor_index == -1 or course_index == -1:
            messagebox.showwarning("Select both", "Please select an instructor and a course.")
            return
        
        selected_instructor = instructors[instructor_index]
        selected_course = courses[course_index]

        if selected_course.instructor and selected_course.instructor.instructor_id == selected_instructor.instructor_id:
            messagebox.showinfo("Already assigned", f"{selected_instructor.name} is already assigned to {selected_instructor.course_name}.")
            return

        if selected_course.instructor and selected_course.instructor.instructor_id != selected_instructor.instructor_id:
            if not messagebox.askyesno("Replace instructor",
                                       f"{selected_course.course_name} already has {selected_course.instructor.name}. Replace?"):
                return

        selected_instructor.assign_course(selected_course)
        selected_course.add_instructor(selected_instructor)

        messagebox.showinfo("Success", f"Assigned {selected_instructor.name} to {selected_course.course_name} - {selected_course.course_name}")
        refresh_cb()
        instructor_box.set("")
        course_box.set("")
        clear_dropdowns(instructor_box, course_box)

    ttk.Button(frame, text="Assign", command=assign_instructor).grid(row=2, column=1, sticky="e", padx=5, pady=10)

    frame.refresh_boxes = refresh_boxes
    return frame
