"""
This module provides the UI for assigning instructors to courses in a Tkinter application,
interacting with an SQLite database.

It allows selecting an instructor and a course from dropdowns and assigning
the former to the latter, with database updates handled by a 'DatabaseManager'.
"""
import tkinter as tk
from tkinter import ttk, messagebox


def clear_dropdowns(instructor_box, course_box):
    """
    Clears the current selection in the instructor and course comboboxes.

    :param instructor_box: The instructor combobox widget.
    :type instructor_box: ttk.Combobox
    :param course_box: The course combobox widget.
    :type course_box: ttk.Combobox
    """
    instructor_box.set("")
    course_box.set("")

def build_assignment_tab(parent, db_manager, refresh_cb):
    """
    Builds the 'Instructor Assignment' tab for the Tkinter UI.

    This tab allows users to assign an instructor to a course. The data is fetched
    from and saved to an SQLite database via the 'db_manager'.

    :param parent: The parent widget (notebook tab).
    :type parent: tk.Widget
    :param db_manager: The manager for database operations.
    :type db_manager: DatabaseManager
    :param refresh_cb: A callback function to refresh the main application's data view
                       after an assignment is made.
    :type refresh_cb: callable
    :return: The frame containing the assignment UI. It includes a 'refresh_boxes'
             method to allow external updates to the dropdowns.
    :rtype: tk.LabelFrame
    """
    frame = tk.LabelFrame(parent, text="Instructor Assignment", padx=10, pady=10)
    frame.pack(padx=20, pady=20, fill="x")

    tk.Label(frame, text="Instructor:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    instructor_box = ttk.Combobox(frame, state="readonly", width=40)
    instructor_box.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame, text="Course:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    course_box = ttk.Combobox(frame, state="readonly", width=40)
    course_box.grid(row=1, column=1, padx=5, pady=5)

    def refresh_boxes():
        """
        Refreshes the values in the instructor and course comboboxes by fetching
        the latest data from the database.
        """
        instructors = db_manager.get_all_instructors()
        courses = db_manager.get_all_courses()
        instructor_box["values"] = [i.display_instructor() for i in instructors]
        course_box["values"] = [c.display_course() for c in courses]
        
        # Store the current lists for later reference
        frame.current_instructors = instructors
        frame.current_courses = courses
        
    def assign_instructor():
        """
        Handles the assignment process when the 'Assign' button is clicked.
        It validates the selection and updates the database.
        """
        instructor_index = instructor_box.current()
        course_index = course_box.current()
        
        if instructor_index == -1 or course_index == -1:
            messagebox.showwarning("Select both", "Please select an instructor and a course.")
            return
        
        selected_instructor = frame.current_instructors[instructor_index]
        selected_course = frame.current_courses[course_index]

        try:
            db_manager.assign_instructor_course(selected_instructor.instructor_id, selected_course.course_id)
            messagebox.showinfo("Success", 
                              f"Assigned {selected_instructor.name} to {selected_course.course_name}")
            refresh_cb()
            instructor_box.set("")
            course_box.set("")
            refresh_boxes()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(frame, text="Assign", command=assign_instructor).grid(row=2, column=1, sticky="e", padx=5, pady=10)

    # Initial load of the boxes
    refresh_boxes()
    
    frame.refresh_boxes = refresh_boxes
    return frame