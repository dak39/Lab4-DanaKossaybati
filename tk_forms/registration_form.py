"""
This module provides the UI for registering students into courses in a Tkinter application.

It allows the user to select a student and a course from dropdown menus and
register the student for the selected course, preventing duplicate registrations.
"""

import tkinter as tk
from tkinter import ttk, messagebox

def build_registration_tab(parent, students, courses, refresh_cb):
    """
    Builds the 'Student Registration' tab for the Tkinter UI.

    This tab contains dropdowns for selecting a student and a course, and a button
    to perform the registration.

    :param parent: The parent widget (notebook tab).
    :type parent: tk.Widget
    :param students: A list of all available student objects.
    :type students: list[Student]
    :param courses: A list of all available course objects.
    :type courses: list[Course]
    :param refresh_cb: A callback function to refresh the main application's data view
                       after a registration is made.
    :type refresh_cb: callable
    :return: The frame containing the registration UI. It includes a 'refresh_boxes'
             method to allow external updates to the dropdowns.
    :rtype: tk.LabelFrame
    """
    
    frame = tk.LabelFrame(parent, text="Student Registration", padx=10, pady=10)
    frame.pack(padx=20, pady=20, fill="x")

    tk.Label(frame, text="Student:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    student_box = ttk.Combobox(frame, state="readonly", width=40,
                               values=[s.display_student() for s in students])
    student_box.grid(row=0, column=1, padx=5, pady=5)
    
    
    tk.Label(frame, text="Course:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    course_box  = ttk.Combobox(frame, state="readonly", width=40,
                               values=[c.display_course() for c in courses])
    course_box.grid(row=1, column=1, padx=5, pady=5)

    def refresh_boxes():
        """
        Refreshes the values in the student and course comboboxes.
        This is called to update the dropdowns when the underlying data changes.
        """
        student_box["values"] = [student.display_student() for student in students]
        course_box["values"]  = [course.display_course() for course in courses]
        student_box.set("")
        course_box.set("")

    def register():
        """
        Handles the registration process when the 'Register' button is clicked.
        It validates the selection, prevents duplicate registrations, and updates
        the data models.
        """
        student_index = student_box.current()
        course_index = course_box.current()
        
        if student_index == -1 or course_index == -1:
            messagebox.showwarning("Select both", "Please select a student and a course.")
            return
        
        selected_student = students[student_index]
        selected_course = courses[course_index]

        # prevent duplicates
        if any(registered_course.course_id == selected_course.course_id for registered_course in getattr(selected_student, "registered_courses", [])):
            messagebox.showinfo("Already registered", f"{selected_student.name} is already in {selected_course.course_id}.")
            return

        selected_student.register_course(selected_course)
        selected_course.add_student(selected_student)

        messagebox.showinfo("Success", f"Registered {selected_student.name} to {selected_course.course_id} - {selected_course.course_name}")
        refresh_cb()
        refresh_boxes()

    ttk.Button(frame, text="Register", command=register).grid(row=2, column=1, sticky="e", padx=5, pady=10)

    # expose for external refresh (when lists change)
    frame.refresh_boxes = refresh_boxes
    return frame
