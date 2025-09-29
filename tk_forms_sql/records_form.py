"""
This module provides the UI for managing records in a Tkinter application using an SQLite database.

It defines functions to build the 'Records' tab, which encapsulates the UI and logic for displaying,
searching, exporting, and backing up records for students, instructors, and courses.
"""
from tkinter import ttk, messagebox, StringVar, filedialog, Frame, Toplevel
from datetime import datetime
import csv

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

def fill_tree(tree, db_manager):
    """
    Populates the Treeview with student, instructor, and course records from the database.

    :param tree: The Treeview widget to populate.
    :type tree: ttk.Treeview
    :param db_manager: The manager for database operations.
    :type db_manager: DatabaseManager
    """
    students = db_manager.get_all_students()
    instructors = db_manager.get_all_instructors()
    courses = db_manager.get_all_courses()
    
    for s in students:
        tree.insert("", "end", values=student_row(s))
    for i in instructors:
        tree.insert("", "end", values=instructor_row(i))
    for c in courses:
        tree.insert("", "end", values=course_row(c))

def refresh_tree(tree, db_manager):
    """
    Clears and refills the Treeview with the latest records from the database.

    :param tree: The Treeview widget to refresh.
    :type tree: ttk.Treeview
    :param db_manager: The manager for database operations.
    :type db_manager: DatabaseManager
    """
    tree.delete(*tree.get_children())
    fill_tree(tree, db_manager)

def apply_search(tree, query_entry, scope_combo, db_manager):
    """
    Filters the records in the Treeview based on a search query and scope.

    :param tree: The Treeview widget to apply the search to.
    :type tree: ttk.Treeview
    :param query_entry: The entry widget containing the search query.
    :type query_entry: tk.Entry
    :param scope_combo: The combobox for selecting the search scope.
    :type scope_combo: ttk.Combobox
    :param db_manager: The manager for database operations.
    :type db_manager: DatabaseManager
    """
    q = query_entry.get().strip().lower()
    scope = scope_combo.get()
    tree.delete(*tree.get_children())
    
    # Get fresh data
    students = []
    instructors = []
    courses = []
    
    if scope in ("All", "Students"):
        students = db_manager.get_all_students()
    if scope in ("All", "Instructors"):
        instructors = db_manager.get_all_instructors()
    if scope in ("All", "Courses"):
        courses = db_manager.get_all_courses()
    
    if not q:
        # Show everything if no search query
        for s in students:
            tree.insert("", "end", values=student_row(s))
        for i in instructors:
            tree.insert("", "end", values=instructor_row(i))
        for c in courses:
            tree.insert("", "end", values=course_row(c))
        return

    def record_matches(row):
        record_type, record_id, name, email = row
        return any(q in str(val).lower() for val in (record_id, name, email))

    # Build filtered results
    rows = []
    rows.extend(student_row(s) for s in students)
    rows.extend(instructor_row(i) for i in instructors)
    rows.extend(course_row(c) for c in courses)

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

def create_backup_dialog(parent, db_manager):
    """
    Opens a dialog window to confirm and create a database backup.

    :param parent: The parent widget for the dialog.
    :type parent: tk.Widget
    :param db_manager: The manager for database operations.
    :type db_manager: DatabaseManager
    """
    dialog = Toplevel(parent)
    dialog.title("Create Database Backup")
    dialog.geometry("400x150")
    dialog.grab_set()
    dialog.transient(parent)

    # Layout
    main_frame = ttk.Frame(dialog, padding=20)
    main_frame.pack(fill="both", expand=True)

    ttk.Label(main_frame, text="Create a backup of the database?").pack(pady=10)

    def create_backup():
        """Initiates the backup process and shows the result."""
        success, message = db_manager.backup_database()
        if success:
            messagebox.showinfo("Backup Success", message)
            dialog.destroy()
        else:
            messagebox.showerror("Backup Failed", message)

    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=20)
    ttk.Button(button_frame, text="Create Backup", command=create_backup).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side="left")

def build_records_tab(parent, db_manager):
    """
    Builds the records management tab for the Tkinter UI.

    This function constructs the entire 'Records' tab, including the search panel,
    the main data table (Treeview), and action buttons for exporting and backups.

    :param parent: The parent widget (notebook tab).
    :type parent: tk.Widget
    :param db_manager: The manager for database operations.
    :type db_manager: DatabaseManager
    :return: The main frame containing the entire records tab UI.
    :rtype: ttk.Frame
    """
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Search Frame
    search_frame = ttk.LabelFrame(frame, text="Search", padding=10)
    search_frame.pack(fill="x", padx=5, pady=5)

    # Search controls
    ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5)
    query_entry = ttk.Entry(search_frame, width=30)
    query_entry.grid(row=0, column=1, padx=5)

    ttk.Label(search_frame, text="Type:").grid(row=0, column=2, padx=5)
    scope_combo = ttk.Combobox(search_frame, values=["All", "Students", "Instructors", "Courses"], 
                              state="readonly", width=15)
    scope_combo.current(0)
    scope_combo.grid(row=0, column=3, padx=5)

    # Buttons frame
    button_frame = ttk.Frame(search_frame)
    button_frame.grid(row=0, column=4, padx=5)

    # Table
    tree_frame = ttk.Frame(frame)
    tree_frame.pack(fill="both", expand=True, pady=10)

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

    # Action buttons below the tree
    action_frame = ttk.Frame(frame)
    action_frame.pack(fill="x", pady=5)

    export_btn = ttk.Button(action_frame, text="Export to CSV",
                           command=lambda: export_to_csv(tree))
    export_btn.pack(side="left", padx=5)

    backup_btn = ttk.Button(action_frame, text="Create Backup",
                           command=lambda: create_backup_dialog(frame, db_manager))
    backup_btn.pack(side="left", padx=5)

    def refresh_records():
        """Refreshes the data in the treeview."""
        refresh_tree(tree, db_manager)

    # Search functionality
    search_btn = ttk.Button(button_frame, text="Search", 
                           command=lambda: apply_search(tree, query_entry, scope_combo, db_manager))
    reset_btn = ttk.Button(button_frame, text="Clear", 
                          command=lambda: reset_search(query_entry, scope_combo, refresh_records))
    refresh_btn = ttk.Button(button_frame, text="Refresh", 
                          command=lambda: refresh_records())

    search_btn.pack(side="left", padx=2)
    reset_btn.pack(side="left", padx=2)
    refresh_btn.pack(side="left", padx=2)

    # Initial load
    fill_tree(tree, db_manager)

    return frame