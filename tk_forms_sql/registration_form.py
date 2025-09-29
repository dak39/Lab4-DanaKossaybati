"""
This module provides the UI for registering students into courses in a Tkinter application,
with data persistence handled by an SQLite database.

It allows selecting a student and a course from dropdowns and registering the student
for the course, with all operations managed through a 'DatabaseManager'.
"""
import tkinter as tk
from tkinter import ttk, messagebox


def build_registration_tab(parent, db_manager, refresh_cb):
    """
    Builds the 'Student Registration' tab for the Tkinter UI.

    This tab allows users to register a student for a course. The data is fetched
    from and saved to an SQLite database via the 'db_manager'.

    :param parent: The parent widget (notebook tab).
    :type parent: tk.Widget
    :param db_manager: The manager for database operations.
    :type db_manager: DatabaseManager
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
    student_box = ttk.Combobox(frame, state="readonly", width=40)
    student_box.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame, text="Course:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    course_box = ttk.Combobox(frame, state="readonly", width=40)
    course_box.grid(row=1, column=1, padx=5, pady=5)

    def refresh_boxes():
        """
        Refreshes the values in the student and course comboboxes by fetching
        the latest data from the database.
        """
        students = db_manager.get_all_students()
        courses = db_manager.get_all_courses()
        student_box["values"] = [student.display_student() for student in students]
        course_box["values"] = [course.display_course() for course in courses]
        student_box.set("")
        course_box.set("")
        
        # Store the current lists for later reference
        frame.current_students = students
        frame.current_courses = courses

    def register():
        """
        Handles the registration process when the 'Register' button is clicked.
        It validates the selection and updates the database.
        """
        student_index = student_box.current()
        course_index = course_box.current()
        
        if student_index == -1 or course_index == -1:
            messagebox.showwarning("Select both", "Please select a student and a course.")
            return
        
        selected_student = frame.current_students[student_index]
        selected_course = frame.current_courses[course_index]

        try:
            db_manager.register_student_course(selected_student.student_id, selected_course.course_id)
            messagebox.showinfo("Success", 
                              f"Registered {selected_student.name} to {selected_course.course_id} - {selected_course.course_name}")
            refresh_cb()
            refresh_boxes()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(frame, text="Register", command=register).grid(row=2, column=1, sticky="e", padx=5, pady=10)

    # Initial load of the boxes
    refresh_boxes()
    
    # expose for external refresh (when lists change)
    frame.refresh_boxes = refresh_boxes
    return frame