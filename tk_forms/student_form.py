"""
This module provides a function to build the 'Add Student' tab for the Tkinter-based GUI.

It includes a form for adding a new student with fields for name, age, email, and student ID.
Input validation is performed before adding the student to the data source.
"""
import tkinter as tk
from tkinter import messagebox
from student import Student

from validators import validate_name, validate_age, require, validate_email, validate_unique_id

def build_student_tab(parent, students, refresh_cb):
    """
    Builds the 'Add Student' tab for the Tkinter application.

    This function creates a LabelFrame containing a form to add a new student.
    The form includes input fields for the student's name, age, email, and student ID.
    An 'Add Student' button triggers validation and the addition of the student.

    :param parent: The parent widget for this tab.
    :type parent: tk.Widget
    :param students: A list of existing Student objects to ensure the new student ID is unique.
    :type students: list
    :param refresh_cb: A callback function to be called after a student is successfully added,
                       to refresh the display of student records.
    :type refresh_cb: function
    :return: The LabelFrame widget containing the student form.
    :rtype: tk.LabelFrame
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
        and adds it to the list of students. Shows a success message
        and clears the input fields. Finally, it calls the refresh callback.
        """
        name  = name_input.get().strip()
        age   = age_input.get().strip()
        email = email_input.get().strip()
        sid   = id_input.get().strip()

        # validate inputs
        if not (validate_name(name) and validate_age(age) and validate_email(email) and require(sid, "Student ID")):
            return

        # check unique ID
        if not validate_unique_id(sid, students, "student_id"):
            return

        student = Student(name=name, age=age, email=email, student_id=sid)
        students.append(student)
        messagebox.showinfo("Success", "Student Added!")


        name_input.delete(0, tk.END)
        age_input.delete(0, tk.END)
        email_input.delete(0, tk.END)
        id_input.delete(0, tk.END)

        refresh_cb()

    tk.Button(frame, text="Add Student", command=add_student).grid(row=4, column=1, pady=10, sticky="e")

    return frame
