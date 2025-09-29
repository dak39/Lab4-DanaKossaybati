"""
This module provides the UI for adding a new instructor in a Tkinter application,
with data persistence handled by an SQLite database.

It includes a form for entering instructor details and handles the creation
of instructor records through a 'DatabaseManager'.
"""
import tkinter as tk
from tkinter import messagebox
from instructor import Instructor
from validators import validate_name, validate_age, validate_email, require
from person import Person

def build_instructor_tab(parent, db_manager, refresh_cb):
    """
    Builds the 'Add Instructor' tab for the Tkinter UI.

    This tab contains input fields for an instructor's details (name, age, email, ID)
    and a button to add the new instructor to the database.

    :param parent: The parent widget (notebook tab).
    :type parent: tk.Widget
    :param db_manager: The manager for database operations.
    :type db_manager: DatabaseManager
    :param refresh_cb: A callback function to refresh the main application's data view
                       after a new instructor is added.
    :type refresh_cb: callable
    """
    frame = tk.LabelFrame(parent, text="Add Instructor", padx=10, pady=10)
    frame.pack(padx=20, pady=20, fill="x")

    tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    name_input = tk.Entry(frame)
    name_input.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame, text="Age:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    age_input = tk.Entry(frame)
    age_input.grid(row=1, column=1, padx=5, pady=5)
    
    tk.Label(frame, text="Email:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    email_input= tk.Entry(frame)
    email_input.grid(row=2, column=1, padx=5, pady=5)
    
    tk.Label(frame, text="Instructor ID:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    id_input   = tk.Entry(frame)
    id_input.grid(row=3, column=1, padx=5, pady=5)

    def add_instructor():
        """
        Handles the logic for adding a new instructor. It retrieves user input,
        validates it, creates an Instructor object, and uses the db_manager to
        add it to the database.
        """
        name = name_input.get().strip()
        age = age_input.get().strip()
        email = email_input.get().strip()
        instructor_id = id_input.get().strip()

        # validate inputs
        if not (validate_name(name) and validate_age(age) and require(age, "age") and 
                validate_email(email) and require(instructor_id, "Instructor ID") and require(name, "Name") and require(email, "Email") and require(age, "Age")):
            return
        
        try:
            instructor = Instructor(name=name, age=age, email=email, instructor_id=instructor_id)
            db_manager.add_instructor(instructor)
            messagebox.showinfo("Success", "Instructor Added!")
            
            name_input.delete(0, tk.END)
            age_input.delete(0, tk.END)
            email_input.delete(0, tk.END)
            id_input.delete(0, tk.END)
            
            refresh_cb()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Add Instructor", command=add_instructor).grid(row=4, column=1, pady=10, sticky="e")