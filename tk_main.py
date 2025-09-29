"""
This module serves as the main entry point for the Tkinter-based School Management System.

It sets up the main application window and builds the tabbed user interface
for managing students, instructors, courses, registrations, and assignments.
Data is managed in-memory and persisted through the forms to JSON files.
"""

import tkinter as tk
from tkinter import ttk

from tk_forms.student_form import build_student_tab
from tk_forms.instructor_form import build_instructor_tab
from tk_forms.course_form import build_course_tab
from tk_forms.registration_form import build_registration_tab
from tk_forms.assignment_form import build_assignment_tab
from tk_forms.records_form import build_records_tab

def main():
    """
    Initializes and runs the Tkinter-based School Management System UI.

    This function sets up the main window, creates the tabbed interface,
    and connects the necessary callbacks to ensure data stays synchronized
    across the different parts of the application.
    """
    root = tk.Tk()
    root.title("School Management System")
    root.geometry("1000x720")

    # In-memory data stores
    students = []
    instructors = []
    courses = []

    # Create tab container
    tabs = ttk.Notebook(root)
    tabs.pack(expand=1, fill="both")

    # Create frames for each tab
    student_tab = ttk.Frame(tabs)
    instructor_tab = ttk.Frame(tabs)
    course_tab = ttk.Frame(tabs)
    registration_tab = ttk.Frame(tabs)
    assignment_tab = ttk.Frame(tabs)
    records_tab = ttk.Frame(tabs)

    tabs.add(student_tab, text="Students")
    tabs.add(instructor_tab, text="Instructors")
    tabs.add(course_tab, text="Courses")
    tabs.add(registration_tab, text="Register Student")
    tabs.add(assignment_tab, text="Assign Instructor")
    tabs.add(records_tab, text="All Records")

    # Build the records tab first to get the refresh_table callback
    tree, refresh_table = build_records_tab(
        records_tab, students, instructors, courses
    )

    # Build registration and assignment tabs
    registration_frame = build_registration_tab(
        registration_tab, students, courses, refresh_table
    )
    assignment_frame = build_assignment_tab(
        assignment_tab, instructors, courses, refresh_table
    )

    def refresh_dropdowns():
        """Refreshes the contents of comboboxes in the registration and assignment tabs."""
        if hasattr(registration_frame, "refresh_boxes"):
            registration_frame.refresh_boxes()
        if hasattr(assignment_frame, "refresh_boxes"):
            assignment_frame.refresh_boxes()
        if hasattr(registration_frame, "clear_dropdowns"):
            registration_frame.clear_dropdowns()
        if hasattr(assignment_frame, "clear_dropdowns"):
            assignment_frame.clear_dropdowns()

    def refresh_all():
        """Refreshes all data views, including the main records table and dropdowns."""
        refresh_table()
        refresh_dropdowns()

    # When data changes in the records table, refresh dropdowns
    if hasattr(tree, 'on_data_change'):
        tree.on_data_change = refresh_dropdowns

    # Build the remaining tabs, passing the refresh_all callback
    build_student_tab(student_tab, students, refresh_all)
    build_instructor_tab(instructor_tab, instructors, refresh_all)
    build_course_tab(course_tab, courses, refresh_all)

    # Set refresh callbacks for registration and assignment forms
    if hasattr(registration_frame, "refresh_cb"):
        registration_frame.refresh_cb = refresh_all
    if hasattr(assignment_frame, "refresh_cb"):
        assignment_frame.refresh_cb = refresh_all

    # Initial data load
    refresh_all()

    root.mainloop()

if __name__ == "__main__":
    main()
