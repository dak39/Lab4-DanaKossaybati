
# School Management System

  

This is a an academic management system implemented with both PyQt5 and Tkinter interfaces, providing dual UI options for managing students, instructors, courses, registrations, and assignments. The system supports both JSON-based and SQLite-based data persistence.

  

## Team

  

-  **Name:** Dana Kossaybati

-  **Email:** dak39@aub.edu.lb

-  **Student ID:** 202205746

-  **Course:** EECE 435L - Software Tools Lab

-  **Section:** Tuesday

  

## Requirements

  

### System Requirements

- Operating System: Windows 10/11 (64-bit)

- Python: 3.12 or higher

  

### Required Libraries

- PyQt5: GUI framework for the Qt interface

- tkinter: Built-in Python GUI framework

- SQLite3: Database management

- Other dependencies: See requirements.txt

  

## Setup and Running Instructions

  

1. Clone the repository:

		git  clone  https://github.com/dak39/Lab4-DanaKossaybati.git

		cd  Lab4-DanaKossaybati

2. Create and activate a virtual environment (recommended):

		python  -m  venv  venv

		.\venv\Scripts\activate

3. Install dependencies:

		pip  install  -r  requirements.txt

4. Run the applications:

	For PyQt interface with JSON storage:

		python  qt_main.py


  

	For PyQt interface with SQLite storage:



		python  qt_main_sql.py


  

	For Tkinter interface with JSON storage:



		python  tk_main.py


  

	For Tkinter interface with SQLite storage:


		python  tk_main_sql.py


  

## Completed Features

- Student management (CRUD operations)

- Instructor management

- Course management

- Registration system

- Assignment system

- Both JSON and SQLite data persistence

- Complete documentation (Sphinx)

  

## Architecture and Design

  

The system follows a modular architecture with separation of concerns:

  

**Data Layer:**

- JSON-based data management (`data_manager.py`)

- SQLite-based data management (`database_manager.py`)

 **Classes Logic:**

- Core entities: `person.py`, `student.py`, `instructor.py`, `course.py`

- Data validation: `validators.py`

  

**Tab Layers:**

- PyQt5 forms (`qt_forms/` and `qt_forms_sql/`)

- Tkinter forms (`tk_forms/` and `tk_forms_sql/`)

  

## References and Citations

  

1. PyQt5 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt5/

2. Tkinter Documentation: https://docs.python.org/3/library/tkinter.html

3. SQLite Documentation: https://www.sqlite.org/docs.html

  

## Academic Honesty

  

I certify that this submission represents my own original work. No other person's work has been used without due acknowledgment. I have not made my work available to anyone else.