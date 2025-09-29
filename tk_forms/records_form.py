"""
This module provides the UI for managing records in a Tkinter application.

It includes functionalities for displaying, searching, editing, deleting,
and importing/exporting records for students, instructors, and courses.
"""
    
from tkinter import ttk, messagebox, Toplevel, StringVar, filedialog
from data_manager import DataManager
import csv
from datetime import datetime
from validators import validate_name, validate_age, validate_email, require, validate_unique_id

STUDENTS_FILE = "students.json"
INSTRUCTORS_FILE = "instructors.json"
COURSES_FILE = "courses.json"

def student_row(s):
    """
    Formats a student object into a tuple for display in a Treeview.

    :param s: The student object.
    :type s: Student
    :return: A tuple containing the student's type, ID, name, and email.
    :rtype: tuple
    """
    return ("Student", s.student_id, s.name, s.get_email())

def instructor_row(i):
    """
    Formats an instructor object into a tuple for display in a Treeview.

    :param i: The instructor object.
    :type i: Instructor
    :return: A tuple containing the instructor's type, ID, name, and email.
    :rtype: tuple
    """
    return ("Instructor", i.instructor_id, i.name, i.get_email())

def course_row(c):
    """
    Formats a course object into a tuple for display in a Treeview.

    :param c: The course object.
    :type c: Course
    :return: A tuple containing the course's type, ID, and name.
    :rtype: tuple
    """
    return ("Course", c.course_id, c.course_name, "-")

def fill_tree(tree, students, instructors, courses):
    """
    Populates the Treeview with student, instructor, and course records.

    :param tree: The Treeview widget to populate.
    :type tree: ttk.Treeview
    :param students: A list of student objects.
    :type students: list[Student]
    :param instructors: A list of instructor objects.
    :type instructors: list[Instructor]
    :param courses: A list of course objects.
    :type courses: list[Course]
    """
    for s in students:
        tree.insert("", "end", values=student_row(s))
    for i in instructors:
        tree.insert("", "end", values=instructor_row(i))
    for c in courses:
        tree.insert("", "end", values=course_row(c))

def refresh_tree(tree, students, instructors, courses):
    """
    Clears and refills the Treeview with the latest records.

    :param tree: The Treeview widget to refresh.
    :type tree: ttk.Treeview
    :param students: A list of student objects.
    :type students: list[Student]
    :param instructors: A list of instructor objects.
    :type instructors: list[Instructor]
    :param courses: A list of course objects.
    :type courses: list[Course]
    """
    tree.delete(*tree.get_children())
    fill_tree(tree, students, instructors, courses)

def apply_search(tree, query_entry, scope_combo, students, instructors, courses):
    """
    Filters the records in the Treeview based on a search query.

    :param tree: The Treeview widget to apply the search to.
    :type tree: ttk.Treeview
    :param query_entry: The entry widget containing the search query.
    :type query_entry: tk.Entry
    :param scope_combo: The combobox for selecting the search scope.
    :type scope_combo: ttk.Combobox
    :param students: A list of all student objects.
    :type students: list[Student]
    :param instructors: A list of all instructor objects.
    :type instructors: list[Instructor]
    :param courses: A list of all course objects.
    :type courses: list[Course]
    """
    
    q = query_entry.get().strip().lower()
    scope = scope_combo.get()
    tree.delete(*tree.get_children())
    
    if not q:
        # Show everything if no search query
        rows = []
        if scope in ("All", "Students"):
            rows += [student_row(s) for s in students]
        if scope in ("All", "Instructors"):
            rows += [instructor_row(i) for i in instructors]
        if scope in ("All", "Courses"):
            rows += [course_row(c) for c in courses]
        
        for r in rows:
            tree.insert("", "end", values=r)
        return

    def record_matches(row):
        record_type, record_id, name, email = row
        
        if (q in str(record_id).lower() or
            q in (name or "").lower() or 
            q in (email or "").lower()):
            return True
        
        return False

    # Build filtered results
    rows = []
    if scope in ("All", "Students"):
        rows += [student_row(student) for student in students]
    if scope in ("All", "Instructors"):
        rows += [instructor_row(instructor) for instructor in instructors]
    if scope in ("All", "Courses"):
        rows += [course_row(course) for course in courses]

    for row in rows:
        if record_matches(row):
            tree.insert("", "end", values=row)

def reset_search(query_entry, scope_combo, refresh_fn):
    """
    Clears the search query and resets the view to show all records.

    :param query_entry: The entry widget for the search query.
    :type query_entry: tk.Entry
    :param scope_combo: The combobox for the search scope.
    :type scope_combo: ttk.Combobox
    :param refresh_fn: The function to call to refresh the records display.
    :type refresh_fn: callable
    """
    query_entry.delete(0, "end")
    scope_combo.current(0)
    refresh_fn()

def export_to_csv(tree):
    """
    Exports the data currently displayed in the Treeview to a CSV file.

    :param tree: The Treeview widget containing the data to export.
    :type tree: ttk.Treeview
    """
    
    # Get all items from the tree
    items = tree.get_children()
    if not items:
        messagebox.showwarning("Export Warning", "No records to export!")
        return

    # Ask user where to save the file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile=f"records_export_{timestamp}.csv"
    )
    
    if not filename:  # User cancelled
        return
        
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write headers
            headers = [tree.heading(col)["text"] for col in tree["columns"]]
            writer.writerow(headers)
            
            # Write data
            for item in items:
                row = tree.item(item)["values"]
                writer.writerow(row)
                
        messagebox.showinfo("Export Successful", f"Records have been exported to {filename}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export records: {str(e)}")

def open_person_edit_dialog(parent, person, person_type, students, instructors, courses, refresh_fn):
    """
    Opens a dialog window to edit the details of a student or instructor.

    :param parent: The parent widget for the dialog.
    :type parent: tk.Widget
    :param person: The person object (Student or Instructor) to edit.
    :type person: Person
    :param person_type: A string indicating the type of person ('student' or 'instructor').
    :type person_type: str
    :param students: A list of all student objects.
    :type students: list[Student]
    :param instructors: A list of all instructor objects.
    :type instructors: list[Instructor]
    :param courses: A list of all course objects.
    :type courses: list[Course]
    :param refresh_fn: A callback function to refresh the main application's data.
    :type refresh_fn: callable
    """
    
    if not person:
        messagebox.showerror("Error", "Person not found.")
        return

    dialog = Toplevel(parent)
    dialog.title(f"Edit {person_type.title()}")
    dialog.geometry("500x280")
    dialog.grab_set()
    dialog.transient(parent)

    # Form variables
    name_var = StringVar(value=person.name)
    age_var = StringVar(value=str(person.age))
    email_var = StringVar(value=person.get_email())
    id_var = StringVar(value=getattr(person, f"{person_type}_id"))

    # Layout
    main_frame = ttk.Frame(dialog, padding=20)
    main_frame.pack(fill="both", expand=True)

    ttk.Label(main_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=5)
    ttk.Entry(main_frame, textvariable=name_var, width=35).grid(row=0, column=1, sticky="ew", padx=(10,0), pady=5)

    ttk.Label(main_frame, text="Age:").grid(row=1, column=0, sticky="w", pady=5)
    ttk.Entry(main_frame, textvariable=age_var, width=10).grid(row=1, column=1, sticky="w", padx=(10,0), pady=5)

    ttk.Label(main_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
    ttk.Entry(main_frame, textvariable=email_var, width=35).grid(row=2, column=1, sticky="ew", padx=(10,0), pady=5)

    ttk.Label(main_frame, text="ID:").grid(row=3, column=0, sticky="w", pady=5)
    ttk.Entry(main_frame, textvariable=id_var, width=20).grid(row=3, column=1, sticky="w", padx=(10,0), pady=5)

    main_frame.columnconfigure(1, weight=1)

    # Buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=4, column=0, columnspan=2, pady=20)

    def save_changes():
        name = name_var.get().strip()
        age_str = age_var.get().strip()
        email = email_var.get().strip()
        new_id = id_var.get().strip()

        # Validation
        if not all([validate_name(name), validate_age(age_str), 
                   validate_email(email), require(new_id, f"{person_type.title()} ID")]):
            return

        # Check ID uniqueness
        id_pool = students if person_type == "student" else instructors
        id_field = f"{person_type}_id"
        if not validate_unique_id(new_id, id_pool, id_field, exclude=person):
            return

        # Save changes
        old_id = getattr(person, id_field)
        person.name = name
        person.age = int(age_str)
        
        try:
            person.set_email(email)
        except Exception as e:
            messagebox.showwarning("Email Error", str(e))
            return

        setattr(person, id_field, new_id)

        # Update course references if ID changed
        if old_id != new_id:
            if person_type == "student":
                for course in courses:
                    for i, student in enumerate(course.enrolled_students):
                        if student is person:
                            course.enrolled_students[i] = person
            else:  # instructor
                for course in courses:
                    if course.instructor is person:
                        course.instructor = person

        dialog.destroy()
        refresh_fn()

    ttk.Button(button_frame, text="Save", command=save_changes).pack(side="right", padx=5)
    ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side="right")

def open_course_edit_dialog(parent, course, students, instructors, courses, refresh_fn):
    """
    Opens a dialog window to edit the details of a course.

    :param parent: The parent widget for the dialog.
    :type parent: tk.Widget
    :param course: The course object to edit.
    :type course: Course
    :param students: A list of all student objects.
    :type students: list[Student]
    :param instructors: A list of all instructor objects.
    :type instructors: list[Instructor]
    :param courses: A list of all course objects.
    :type courses: list[Course]
    :param refresh_fn: A callback function to refresh the main application's data.
    :type refresh_fn: callable
    """
    
    if not course:
        messagebox.showerror("Error", "Course not found.")
        return

    dialog = Toplevel(parent)
    dialog.title("Edit Course")
    dialog.geometry("400x180")
    dialog.grab_set()
    dialog.transient(parent)

    id_var = StringVar(value=course.course_id)
    name_var = StringVar(value=course.course_name)

    main_frame = ttk.Frame(dialog, padding=20)
    main_frame.pack(fill="both", expand=True)

    ttk.Label(main_frame, text="Course ID:").grid(row=0, column=0, sticky="w", pady=8)
    ttk.Entry(main_frame, textvariable=id_var, width=25).grid(row=0, column=1, padx=(10,0), pady=8)

    ttk.Label(main_frame, text="Course Name:").grid(row=1, column=0, sticky="w", pady=8)
    ttk.Entry(main_frame, textvariable=name_var, width=25).grid(row=1, column=1, padx=(10,0), pady=8)

    def save_course():
        """Saves changes to the course. Updated references if ID changed."""
        old_id = course.course_id
        new_id = id_var.get().strip()
        new_name = name_var.get().strip()

        if not (require(new_id, "Course ID") and require(new_name, "Course Name")):
            return

        if not validate_unique_id(new_id, courses, "course_id", exclude=course):
            return

        course.course_id = new_id
        course.course_name = new_name

        # Update references in student/instructor lists
        if old_id != new_id:
            for student in students:
                for i, c in enumerate(student.registered_courses):
                    if c.course_id == old_id:
                        student.registered_courses[i] = new_id
            for instructor in instructors:
                for i, c in enumerate(instructor.assigned_courses):
                    if c.course_id == old_id:
                        instructor.assigned_courses[i] = new_id

        dialog.destroy()
        refresh_fn()

    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=2, column=0, columnspan=2, pady=15)
    ttk.Button(button_frame, text="Save", command=save_course).pack(side="right", padx=5)
    ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side="right")

def edit_selected(tree, parent, students, instructors, courses, refresh_fn):
    """
    Opens an edit dialog for the currently selected item in the Treeview.

    :param tree: The Treeview widget.
    :type tree: ttk.Treeview
    :param parent: The parent widget for the dialog.
    :type parent: tk.Widget
    :param students: A list of all student objects.
    :type students: list[Student]
    :param instructors: A list of all instructor objects.
    :type instructors: list[Instructor]
    :param courses: A list of all course objects.
    :type courses: list[Course]
    :param refresh_fn: A callback function to refresh the main application's data.
    :type refresh_fn: callable
    """
    
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("No Selection", "Please select a record to edit.")
        return

    record_type, record_id, *_ = tree.item(selection[0], "values")

    if record_type == "Student":
        person = next((s for s in students if str(s.student_id) == str(record_id)), None)
        open_person_edit_dialog(parent, person, "student", students, instructors, courses, refresh_fn)
    elif record_type == "Instructor":
        person = next((i for i in instructors if str(i.instructor_id) == str(record_id)), None)
        open_person_edit_dialog(parent, person, "instructor", students, instructors, courses, refresh_fn)
    elif record_type == "Course":
        course = next((c for c in courses if str(c.course_id) == str(record_id)), None)
        open_course_edit_dialog(parent, course, students, instructors, courses, refresh_fn)

def delete_selected(tree, students, instructors, courses, refresh_fn):
    """
    Deletes the currently selected item from the Treeview and the data lists.

    :param tree: The Treeview widget.
    :type tree: ttk.Treeview
    :param students: A list of all student objects.
    :type students: list[Student]
    :param instructors: A list of all instructor objects.
    :type instructors: list[Instructor]
    :param courses: A list of all course objects.
    :type courses: list[Course]
    :param refresh_fn: A callback function to refresh the main application's data.
    :type refresh_fn: callable
    """
    
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("No Selection", "Please select a record to delete.")
        return

    record_type, record_id, *_ = tree.item(selection[0], "values")
    
    if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {record_type} {record_id}?"):
        return

    if record_type == "Student":
        student = next((s for s in students if str(s.student_id) == str(record_id)), None)
        if student:
            # Remove from course enrollments
            for course in courses:
                if student in course.enrolled_students:
                    course.enrolled_students.remove(student)
            students.remove(student)

    elif record_type == "Instructor":
        instructor = next((i for i in instructors if str(i.instructor_id) == str(record_id)), None)
        if instructor:
            # Remove instructor assignments
            for course in courses:
                if course.instructor is instructor:
                    course.instructor = None
            instructors.remove(instructor)

    elif record_type == "Course":
        course = next((c for c in courses if str(c.course_id) == str(record_id)), None)
        if course:
            # Remove from student/instructor lists
            for student in students:
                if course.course_id in student.registered_courses:
                    student.registered_courses.remove(course.course_id)
            for instructor in instructors:
                if course.course_id in instructor.assigned_courses:
                    instructor.assigned_courses.remove(course.course_id)
            courses.remove(course)

    refresh_fn()

def save_all(students, instructors, courses):
    """
    Saves all student, instructor, and course data to their respective JSON files.

    :param students: A list of all student objects.
    :type students: list[Student]
    :param instructors: A list of all instructor objects.
    :type instructors: list[Instructor]
    :param courses: A list of all course objects.
    :type courses: list[Course]
    """
    
    try:
        DataManager.save_data(STUDENTS_FILE, students, "student_id")
        DataManager.save_data(INSTRUCTORS_FILE, instructors, "instructor_id")
        DataManager.save_data(COURSES_FILE, courses, "course_id")
        messagebox.showinfo("Success", "All data has been saved.")
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save data: {str(e)}")

def load_all(students, instructors, courses, refresh_fn):
    """
    Loads all student, instructor, and course data from their respective JSON files.

    :param students: A list to be populated with student objects.
    :type students: list[Student]
    :param instructors: A list to be populated with instructor objects.
    :type instructors: list[Instructor]
    :param courses: A list to be populated with course objects.
    :type courses: list[Course]
    :param refresh_fn: A callback function to refresh the main application's data.
    :type refresh_fn: callable
    """
    try:
        from student import Student
        from instructor import Instructor
        from course import Course

        # Load data from files
        student_data = DataManager.load_json(STUDENTS_FILE)
        instructor_data = DataManager.load_json(INSTRUCTORS_FILE)
        course_data = DataManager.load_json(COURSES_FILE)
        

        # Create objects
        loaded_students = [Student.from_dict(d) for d in student_data]
        loaded_instructors = [Instructor.from_dict(d) for d in instructor_data]
        loaded_courses = [Course.from_dict(d) for d in course_data]

        existing_students = {s.student_id for s in students}
        existing_instructors = {i.instructor_id for i in instructors}
        existing_courses = {c.course_id for c in courses}

        # Add new records (skip duplicates)
        for student in loaded_students:
            if student.student_id not in existing_students:
                students.append(student)
                existing_students.add(student.student_id)

        for instructor in loaded_instructors:
            if instructor.instructor_id not in existing_instructors:
                instructors.append(instructor)
                existing_instructors.add(instructor.instructor_id)

        for course in loaded_courses:
            if course.course_id not in existing_courses:
                courses.append(course)
                existing_courses.add(course.course_id)

        refresh_fn()
        messagebox.showinfo("Success", "Data loaded successfully.")

    except FileNotFoundError:
        messagebox.showwarning("Files Not Found", "One or more data files could not be found.")
    except Exception as e:
        messagebox.showerror("Load Error", f"Failed to load data: {str(e)}")

def build_records_tab(parent, students, instructors, courses, on_data_change=None):
    """
    Builds the records management tab for the Tkinter UI.

    :param parent: The parent widget.
    :type parent: tk.Widget
    :param students: A list of all student objects.
    :type students: list[Student]
    :param instructors: A list of all instructor objects.
    :type instructors: list[Instructor]
    :param courses: A list of all course objects.
    :type courses: list[Course]
    :param on_data_change: An optional callback function to be called when data changes.
    :type on_data_change: callable, optional
    :return: A tuple containing the Treeview widget and a refresh function.
    :rtype: tuple(ttk.Treeview, callable)
    """
    
    # Search controls
    search_frame = ttk.Frame(parent)
    search_frame.pack(fill="x", padx=10, pady=8)

    ttk.Label(search_frame, text="Search:").pack(side="left", padx=(0, 8))
    
    query_entry = ttk.Entry(search_frame, width=30)
    query_entry.pack(side="left", padx=(0, 8))

    scope_combo = ttk.Combobox(search_frame, values=["All", "Students", "Instructors", "Courses"], 
                              state="readonly", width=12)
    scope_combo.current(0)
    scope_combo.pack(side="left", padx=(0, 8))

    ttk.Button(search_frame, text="Search", 
              command=lambda: apply_search(tree, query_entry, scope_combo, students, instructors, courses)
              ).pack(side="left", padx=(0, 5))

    ttk.Button(search_frame, text="Clear", 
              command=lambda: reset_search(query_entry, scope_combo, refresh_function)
              ).pack(side="left")

    # Action buttons
    action_frame = ttk.Frame(parent)
    action_frame.pack(fill="x", padx=10, pady=(0, 8))

    ttk.Button(action_frame, text="Edit", 
              command=lambda: edit_selected(tree, parent, students, instructors, courses, refresh_function)
              ).pack(side="left", padx=(0, 5))

    ttk.Button(action_frame, text="Delete", 
              command=lambda: delete_selected(tree, students, instructors, courses, refresh_function)
              ).pack(side="left", padx=(0, 5))

    ttk.Button(action_frame, text="Save All", 
              command=lambda: save_all(students, instructors, courses)
              ).pack(side="left", padx=(0, 5))

    ttk.Button(action_frame, text="Load All", 
              command=lambda: load_all(students, instructors, courses, refresh_function)
              ).pack(side="left", padx=(0, 5))

    ttk.Button(action_frame, text="Export to CSV", 
              command=lambda: export_to_csv(tree)
              ).pack(side="left")
    
    # Table
    tree_frame = ttk.Frame(parent)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    tree = ttk.Treeview(tree_frame, columns=("Type", "ID", "Name", "Email"), 
                        show="headings", height=15)

    # Configure headings
    tree.heading("Type", text="Type")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")

    # Configure columns
    tree.column("Type", width=100)
    tree.column("ID", width=100)
    tree.column("Name", width=200)
    tree.column("Email", width=200)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refresh_function():
        refresh_tree(tree, students, instructors, courses)
        if hasattr(tree, "on_data_change") and callable(tree.on_data_change):
            tree.on_data_change()

    # Initial load
    fill_tree(tree, students, instructors, courses)

    return tree, refresh_function

    # Main table
    tree = ttk.Treeview(parent, columns=("Type", "ID", "Name", "Email"), show="headings")
    
    for col in ("Type", "ID", "Name", "Email"):
        tree.heading(col, text=col)
        if col == "Email":
            tree.column(col, width=250)
        else:
            tree.column(col, width=140)

    tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    tree.on_data_change = on_data_change
    def refresh_function():
        refresh_tree(tree, students, instructors, courses)
        cb = getattr(tree, "on_data_change", None)
        if callable(cb):
            cb()

    # Initial population
    refresh_function()

    return tree, refresh_function