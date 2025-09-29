"""
This module provides a function to build the 'Add Student' tab for the Tkinter-based GUI,
interacting with an SQLite database.
"""
import tkinter as tk
from tkinter import messagebox
from student import Student
from validators import validate_name, validate_age, require, validate_email

def build_student_tab(parent, db_manager, refresh_cb):
    """
    Builds the 'Add Student' tab for the Tkinter application.

    This function creates a LabelFrame containing a form to add a new student.
    The form includes input fields for the student's name, age, email, and student ID.
    An 'Add Student' button triggers validation and saves the student to the database.

    :param parent: The parent widget for this tab.
    :type parent: tk.Widget
    :param db_manager: The database manager instance for database operations.
    :type db_manager: DatabaseManager
    :param refresh_cb: A callback function to be called after a student is successfully added,
                       to refresh the display of student records.
    :type refresh_cb: function
    """
    frame = tk.LabelFrame(parent, text="Add Student", padx=10, pady=10)
    frame.pack(padx=20, pady=20, fill="x")

    tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    tk.Label(frame, text="Age:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    tk.Label(frame, text="Email:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    tk.Label(frame, text="Student ID:").grid(row=3, column=0, sticky="w", padx=5, pady=5)

    name_input = tk.Entry(frame)
    age_input  = tk.Entry(frame)
    email_input= tk.Entry(frame)
    id_input   = tk.Entry(frame)

    name_input.grid(row=0, column=1, padx=5, pady=5)
    age_input.grid(row=1, column=1, padx=5, pady=5)
    email_input.grid(row=2, column=1, padx=5, pady=5)
    id_input.grid(row=3, column=1, padx=5, pady=5)

    def add_student():
        """
        Handles the 'Add Student' button click event.

        Retrieves user input, validates it, creates a new Student object,
        and adds it to the database. Shows a success or error message
        and clears the input fields. Finally, it calls the refresh callback.
        """
        name  = name_input.get().strip()
        age   = age_input.get().strip()
        email = email_input.get().strip()
        sid   = id_input.get().strip()

        # validate inputs
        if not (validate_name(name) and validate_age(age) and validate_email(email) and require(sid, "Student ID")):
            return

        try:
            student = Student(name=name, age=age, email=email, student_id=sid)
            db_manager.add_student(student)
            messagebox.showinfo("Success", "Student Added!")

            name_input.delete(0, tk.END)
            age_input.delete(0, tk.END)
            email_input.delete(0, tk.END)
            id_input.delete(0, tk.END)

            refresh_cb()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Add Student", command=add_student).grid(row=4, column=1, pady=10, sticky="e")
    
    return frame