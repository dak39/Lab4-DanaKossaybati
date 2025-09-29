"""
This module provides functions to build the 'Records' tab for the PyQt5-based GUI.

It includes functionality for displaying, searching, filtering, and exporting student,
instructor, and course records from the database. It also provides an option to create
a backup of the database.
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QComboBox, QDialog, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
)
import csv
from datetime import datetime

def student_row(student):
    """
    Formats a student object into a tuple for display in the records tree.

    :param student: The student object.
    :type student: Student
    :return: A tuple containing the student's details.
    :rtype: tuple
    """
    return ("Student", student.student_id, student.name, student.get_email())

def instructor_row(instructor):
    """
    Formats an instructor object into a tuple for display in the records tree.

    :param instructor: The instructor object.
    :type instructor: Instructor
    :return: A tuple containing the instructor's details.
    :rtype: tuple
    """
    return ("Instructor", instructor.instructor_id, instructor.name, instructor.get_email())

def course_row(course):
    """
    Formats a course object into a tuple for display in the records tree.

    :param course: The course object.
    :type course: Course
    :return: A tuple containing the course's details.
    :rtype: tuple
    """
    return ("Course", course.course_id, course.course_name, "-")

def insert_row(tree, row):
    """
    Inserts a new row into the specified QTreeWidget.

    :param tree: The QTreeWidget to insert the row into.
    :type tree: QTreeWidget
    :param row: A tuple or list of data for the row.
    :type row: tuple or list
    """
    item = QTreeWidgetItem([str(x) if x is not None else "" for x in row])
    tree.addTopLevelItem(item)

def fill_tree(tree, db_manager):
    """
    Populates the QTreeWidget with all records from the database.

    :param tree: The QTreeWidget to populate.
    :type tree: QTreeWidget
    :param db_manager: The database manager instance.
    :type db_manager: DatabaseManager
    """
    students = db_manager.get_all_students()
    instructors = db_manager.get_all_instructors()
    courses = db_manager.get_all_courses()

    for student in students:
        insert_row(tree, student_row(student))
    for instructor in instructors:
        insert_row(tree, instructor_row(instructor))
    for course in courses:
        insert_row(tree, course_row(course))

def refresh_tree(tree, db_manager):
    """
    Clears and refills the QTreeWidget with fresh data from the database.

    :param tree: The QTreeWidget to refresh.
    :type tree: QTreeWidget
    :param db_manager: The database manager instance.
    :type db_manager: DatabaseManager
    """
    tree.clear()
    fill_tree(tree, db_manager)

def apply_search(tree, query_entry, scope_combo, db_manager):
    """
    Filters the records in the tree based on a search query and scope.

    :param tree: The QTreeWidget to apply the search to.
    :type tree: QTreeWidget
    :param query_entry: The QLineEdit widget containing the search query.
    :type query_entry: QLineEdit
    :param scope_combo: The QComboBox widget for the search scope.
    :type scope_combo: QComboBox
    :param db_manager: The database manager instance.
    :type db_manager: DatabaseManager
    """
    search_input = query_entry.text().strip().lower()
    scope = scope_combo.currentText()
    tree.clear()

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

    if not search_input:
        # Show everything if no search query
        for student in students:
            insert_row(tree, student_row(student))
        for instructor in instructors:
            insert_row(tree, instructor_row(instructor))
        for course in courses:
            insert_row(tree, course_row(course))
        return

    def record_matches(row):
        record_type, record_id, name, email = row
        return any(search_input in str(val).lower() for val in (record_id, name, email))

    # Build filtered results
    rows = []
    rows.extend(student_row(s) for s in students)
    rows.extend(instructor_row(i) for i in instructors)
    rows.extend(course_row(c) for c in courses)

    for row in rows:
        if record_matches(row):
            insert_row(tree, row)

def export_to_csv(tree):
    """
    Exports the currently displayed records in the QTreeWidget to a CSV file.

    :param tree: The QTreeWidget containing the records to export.
    :type tree: QTreeWidget
    """
    top_count = tree.topLevelItemCount()
    if top_count == 0:
        QMessageBox.warning(tree, "Export Warning", "No records to export!")
        return

    # Ask user where to save the file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suggested = f"records_export_{timestamp}.csv"
    filename, _ = QFileDialog.getSaveFileName(
        tree, "Save CSV", suggested, "CSV files (*.csv)"
    )

    if not filename:
        return

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write headers
            headers = [tree.headerItem().text(col) for col in range(tree.columnCount())]
            writer.writerow(headers)

            # Write data
            for i in range(top_count):
                item = tree.topLevelItem(i)
                row = [item.text(col) for col in range(tree.columnCount())]
                writer.writerow(row)

        QMessageBox.information(tree, "Export Successful",
                              f"Records have been exported to {filename}")
    except Exception as e:
        QMessageBox.critical(tree, "Export Error",
                           f"Failed to export records: {str(e)}")

def create_backup_dialog(parent, db_manager):
    """
    Opens a dialog to confirm and create a backup of the database.

    :param parent: The parent widget for the dialog.
    :type parent: QWidget
    :param db_manager: The database manager instance.
    :type db_manager: DatabaseManager
    """
    dialog = QDialog(parent)
    dialog.setWindowTitle("Create Database Backup")
    dialog.setModal(True)
    dialog.resize(400, 150)

    layout = QVBoxLayout(dialog)

    # Message
    layout.addWidget(QLabel("Create a backup of the database?"))

    # Buttons
    button_frame = QWidget(dialog)
    button_layout = QHBoxLayout(button_frame)
    button_layout.addStretch(1)

    def create_backup():
        success, message = db_manager.backup_database()
        if success:
            QMessageBox.information(dialog, "Backup Success", message)
            dialog.accept()
        else:
            QMessageBox.critical(dialog, "Backup Failed", message)

    backup_button = QPushButton("Create Backup", button_frame)
    backup_button.clicked.connect(create_backup)
    cancel_button = QPushButton("Cancel", button_frame)
    cancel_button.clicked.connect(dialog.reject)

    button_layout.addWidget(cancel_button)
    button_layout.addWidget(backup_button)
    layout.addWidget(button_frame)

    dialog.exec_()

def reset_search(query_entry, scope_combo, refresh_callback):
    """
    Resets the search fields and refreshes the tree view.

    :param query_entry: The QLineEdit widget for the search query.
    :type query_entry: QLineEdit
    :param scope_combo: The QComboBox for the search scope.
    :type scope_combo: QComboBox
    :param refresh_callback: The function to call to refresh the records view.
    :type refresh_callback: function
    """
    query_entry.clear()
    scope_combo.setCurrentIndex(0)  # "All"
    refresh_callback()

def build_records_tab(parent, db_manager):
    """
    Builds the 'Records' tab, which displays all records and provides search and export functionality.

    :param parent: The parent widget for this tab.
    :type parent: QWidget
    :param db_manager: The database manager instance.
    :type db_manager: DatabaseManager
    :return: The main widget for the 'Records' tab.
    :rtype: QWidget
    """
    main_widget = QWidget(parent)
    layout = QVBoxLayout(main_widget)
    layout.setContentsMargins(10, 10, 10, 10)

    # Search frame
    search_frame = QWidget(main_widget)
    search_layout = QHBoxLayout(search_frame)
    search_layout.setContentsMargins(0, 0, 0, 0)

    search_layout.addWidget(QLabel("Search:"))
    query_entry = QLineEdit(search_frame)
    search_layout.addWidget(query_entry)

    search_layout.addWidget(QLabel("Type:"))
    scope_combo = QComboBox(search_frame)
    scope_combo.addItems(["All", "Students", "Instructors", "Courses"])
    search_layout.addWidget(scope_combo)

    layout.addWidget(search_frame)

    # Tree widget
    tree = QTreeWidget(main_widget)
    tree.setHeaderLabels(["Type", "ID", "Name", "Email"])
    tree.setColumnWidth(0, 100)
    tree.setColumnWidth(1, 100)
    tree.setColumnWidth(2, 200)
    tree.setColumnWidth(3, 200)
    layout.addWidget(tree)

    # Button frame
    button_frame = QWidget(main_widget)
    button_layout = QHBoxLayout(button_frame)
    button_layout.setContentsMargins(0, 0, 0, 0)

    def refresh_records():
        refresh_tree(tree, db_manager)

    # Search buttons
    search_button = QPushButton("Search", search_frame)
    search_button.clicked.connect(lambda: apply_search(tree, query_entry, scope_combo, db_manager))
    search_layout.addWidget(search_button)

    reset_button = QPushButton("Clear", search_frame)
    reset_button.clicked.connect(lambda: reset_search(query_entry, scope_combo, refresh_records))
    search_layout.addWidget(reset_button)

    refresh_button = QPushButton("Refresh", search_frame)
    refresh_button.clicked.connect(refresh_records)
    search_layout.addWidget(refresh_button)

    # Export and backup buttons
    export_button = QPushButton("Export to CSV", button_frame)
    export_button.clicked.connect(lambda: export_to_csv(tree))
    button_layout.addWidget(export_button)

    backup_button = QPushButton("Create Backup", button_frame)
    backup_button.clicked.connect(lambda: create_backup_dialog(main_widget, db_manager))
    button_layout.addWidget(backup_button)

    button_layout.addStretch(1)
    layout.addWidget(button_frame)

    # Initial load
    fill_tree(tree, db_manager)

    return main_widget