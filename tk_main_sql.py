"""
This module serves as the main entry point for the Tkinter-based School Management System,
which uses an SQLite database for data persistence.

It sets up the main application window, initializes the database manager, and builds the
tabbed user interface for managing students, instructors, courses, registrations, and assignments.
"""

import tkinter as tk
from tkinter import ttk

from tk_forms_sql.student_form import build_student_tab
from tk_forms_sql.instructor_form import build_instructor_tab
from tk_forms_sql.course_form import build_course_tab
from tk_forms_sql.registration_form import build_registration_tab
from tk_forms_sql.assignment_form import build_assignment_tab
from tk_forms_sql.records_form import build_records_tab

from database_manager import DatabaseManager

class MainWindow:
    """
    The main window of the application, which contains the tabbed interface.

    :param title: The title of the main window.
    :type title: str
    """
    def __init__(self, title="School Management System - SQLite"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("800x600")
        
        # Initialize database manager
        self.db_manager = DatabaseManager()

        # Build the UI
        self.build_ui()

    def build_ui(self):
        """
        Constructs the user interface, including the tab control and all the individual tabs.
        """
        # Create tab control
        tab_control = ttk.Notebook(self.root)
        
        # Create tabs
        student_tab = ttk.Frame(tab_control)
        instructor_tab = ttk.Frame(tab_control)
        course_tab = ttk.Frame(tab_control)
        registration_tab = ttk.Frame(tab_control)
        assignment_tab = ttk.Frame(tab_control)
        records_tab = ttk.Frame(tab_control)
        
        # Add tabs to tab control
        tab_control.add(student_tab, text="Students")
        tab_control.add(instructor_tab, text="Instructors")
        tab_control.add(course_tab, text="Courses")
        tab_control.add(registration_tab, text="Registration")
        tab_control.add(assignment_tab, text="Assignment")
        tab_control.add(records_tab, text="Records")
        
        # Build each tab
        def refresh_all():
            """
            Refreshes the data in all relevant tabs to ensure the UI is up-to-date.
            """
            if hasattr(registration_form, 'refresh_boxes'):
                registration_form.refresh_boxes()
            if hasattr(assignment_form, 'refresh_boxes'):
                assignment_form.refresh_boxes()
            if hasattr(records_frame, 'refresh_records'):
                records_frame.refresh_records()

        # Build tabs and store references to forms where needed
        build_student_tab(student_tab, self.db_manager, refresh_all)
        build_instructor_tab(instructor_tab, self.db_manager, refresh_all)
        build_course_tab(course_tab, self.db_manager, refresh_all)
        registration_form = build_registration_tab(registration_tab, self.db_manager, refresh_all)
        assignment_form = build_assignment_tab(assignment_tab, self.db_manager, refresh_all)
        records_frame = build_records_tab(records_tab, self.db_manager)
        
        tab_control.pack(expand=1, fill="both")

        # Initial load
        refresh_all()

    def run(self):
        """
        Starts the Tkinter main event loop.
        """
        self.root.mainloop()

def main():
    """
    The main function to run the Tkinter application.
    """
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main()