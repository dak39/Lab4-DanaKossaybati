"""
This module provides the UI for adding a new course in a Tkinter application,
with data persistence handled by an SQLite database.

It includes a form for entering course details and handles the creation
of course records through a 'DatabaseManager'.
"""
import tkinter as tk
from tkinter import messagebox
from course import Course
from validators import require

def build_course_tab(parent, db_manager, refresh_cb):
    """
    Builds the 'Add Course' tab for the Tkinter UI.

    This tab contains input fields for a course's ID and name, and a button
    to add the new course to the database.

    :param parent: The parent widget (notebook tab).
    :type parent: tk.Widget
    :param db_manager: The manager for database operations.
    :type db_manager: DatabaseManager
    :param refresh_cb: A callback function to refresh the main application's data view
                       after a new course is added.
    :type refresh_cb: callable
    """
    frame = tk.LabelFrame(parent, text="Add Course", padx=10, pady=10)
    frame.pack(padx=20, pady=20, fill="x")

    tk.Label(frame, text="Course ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    id_input = tk.Entry(frame)
    id_input.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame, text="Course Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    name_input = tk.Entry(frame)
    name_input.grid(row=1, column=1, padx=5, pady=5)


    def add_course():
        """
        Handles the logic for adding a new course. It retrieves user input,
        validates it, creates a Course object, and uses the db_manager to
        add it to the database.
        """
        course_id = id_input.get().strip()
        course_name = name_input.get().strip()
        
        # make sure that the user filed the required fields
        if not (require(course_id, "Course ID") and 
                require(course_name, "Course Name")):
            return
        
        
        try:
            course = Course(course_id=course_id, course_name=course_name)
            db_manager.add_course(course)
            messagebox.showinfo("Success", "Course Added!")
            id_input.delete(0, tk.END)
            name_input.delete(0, tk.END)

            refresh_cb()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Add Course", command=add_course).grid(row=3, column=1, pady=10, sticky="e")