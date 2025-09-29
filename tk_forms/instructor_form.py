"""
This module provides the UI for adding a new instructor in a Tkinter application.
"""

import tkinter as tk
from tkinter import messagebox
from instructor import Instructor
from validators import validate_name, validate_age, validate_email, require, validate_unique_id
from person import Person

def build_instructor_tab(parent, instructors, refresh_cb):
    """
    Builds the instructor creation tab for the Tkinter UI.

    :param parent: The parent widget.
    :type parent: tk.Widget
    :param instructors: A list of all instructor objects.
    :type instructors: list[Instructor]
    :param refresh_cb: A callback function to refresh the main application's data.
    :type refresh_cb: callable
    :return: The frame containing the instructor creation tab's UI.
    :rtype: tk.LabelFrame
    """
    frame = tk.LabelFrame(parent, text="Add Instructor", padx=10, pady=10)
    frame.pack(padx=20, pady=20, fill="x")

    tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    name_input = tk.Entry(frame)
    name_input.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame, text="Age:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    age_input  = tk.Entry(frame)
    age_input.grid(row=1, column=1, padx=5, pady=5)
    
    tk.Label(frame, text="Email:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    email_input= tk.Entry(frame)
    email_input.grid(row=2, column=1, padx=5, pady=5)
    
    tk.Label(frame, text="Instructor ID:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    id_input   = tk.Entry(frame)
    id_input.grid(row=3, column=1, padx=5, pady=5)

    def add_instructor():
        """
        Handles the logic for adding a new instructor.
        """
        name  = name_input.get().strip()
        age   = age_input.get().strip()
        email = email_input.get().strip()
        iid   = id_input.get().strip()

        # validate inpts
        if not (validate_name(name) and validate_age(age) and validate_email(email) and require(iid, "Instructor ID")):
            return
        
        # check unique ID
        if not validate_unique_id(iid, instructors, "instructor_id"):
            return

        instructor = Instructor(name=name, age=age, email=email, instructor_id=iid)
        instructors.append(instructor)
        messagebox.showinfo("Success", "Instructor Added!")
        
        name_input.delete(0, tk.END)
        age_input.delete(0, tk.END)
        email_input.delete(0, tk.END)
        id_input.delete(0, tk.END)
        
        refresh_cb()

    tk.Button(frame, text="Add Instructor", command=add_instructor).grid(row=4, column=1, pady=10, sticky="e")
    return frame
