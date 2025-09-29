"""
This module provides the UI for managing records in a PyQt5 application.

It includes functionalities for displaying, searching, editing, deleting,
and importing/exporting records for students, instructors, and courses,
with data managed in-memory.
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QComboBox, QDialog, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
)
from data_manager import DataManager
import csv
from datetime import datetime
from validators import validate_name, validate_age, validate_email, require, validate_unique_id

STUDENTS_FILE = "students.json"
INSTRUCTORS_FILE = "instructors.json"
COURSES_FILE = "courses.json"


def student_row(student):
    """
    Formats a student object into a tuple for display.

    :param student: The student object.
    :type student: Student
    :return: A tuple of student's details.
    :rtype: tuple
    """
    return ("Student", student.student_id, student.name, student.get_email())


def instructor_row(instructor):
    """
    Formats an instructor object into a tuple for display.

    :param instructor: The instructor object.
    :type instructor: Instructor
    :return: A tuple of instructor's details.
    :rtype: tuple
    """
    return ("Instructor", instructor.instructor_id, instructor.name, instructor.get_email())


def course_row(course):
    """
    Formats a course object into a tuple for display.

    :param course: The course object.
    :type course: Course
    :return: A tuple of course's details.
    :rtype: tuple
    """
    return ("Course", course.course_id, course.course_name, "-")


def insert_row(tree, row):
    """
    Inserts a new row into the tree widget.

    :param tree: The QTreeWidget to insert into.
    :type tree: QTreeWidget
    :param row: A tuple of data for the row.
    :type row: tuple
    """
    item = QTreeWidgetItem([str(x) if x is not None else "" for x in row])
    tree.addTopLevelItem(item)


def fill_tree(tree, students, instructors, courses):
    """
    Populates the tree widget with all records.

    :param tree: The QTreeWidget to populate.
    :type tree: QTreeWidget
    :param students: List of student objects.
    :type students: list[Student]
    :param instructors: List of instructor objects.
    :type instructors: list[Instructor]
    :param courses: List of course objects.
    :type courses: list[Course]
    """
    for student in students:
        insert_row(tree, student_row(student))
    for instructor in instructors:
        insert_row(tree, instructor_row(instructor))
    for course in courses:
        insert_row(tree, course_row(course))


def refresh_tree(tree, students, instructors, courses):
    """
    Clears and refills the tree widget with the latest data.

    :param tree: The QTreeWidget to refresh.
    :type tree: QTreeWidget
    :param students: List of student objects.
    :type students: list[Student]
    :param instructors: List of instructor objects.
    :type instructors: list[Instructor]
    :param courses: List of course objects.
    :type courses: list[Course]
    """
    tree.clear()
    fill_tree(tree, students, instructors, courses)


def apply_search(tree, query_entry, scope_combo, students, instructors, courses):
    """
    Filters the records in the tree widget based on a search query.

    :param tree: The QTreeWidget to search in.
    :type tree: QTreeWidget
    :param query_entry: The QLineEdit with the search query.
    :type query_entry: QLineEdit
    :param scope_combo: The QComboBox for search scope.
    :type scope_combo: QComboBox
    :param students: List of student objects.
    :type students: list[Student]
    :param instructors: List of instructor objects.
    :type instructors: list[Instructor]
    :param courses: List of course objects.
    :type courses: list[Course]
    """
    search_input = query_entry.text().strip().lower()
    scope = scope_combo.currentText()
    tree.clear()

    if not search_input:
        # Show everything if no search query
        rows = []
        if scope in ("All", "Students"):
            rows += [student_row(student) for student in students]
        if scope in ("All", "Instructors"):
            rows += [instructor_row(instructor) for instructor in instructors]
        if scope in ("All", "Courses"):
            rows += [course_row(course) for course in courses]

        for r in rows:
            insert_row(tree, r)
        return


    def record_matches(row):
        record_type, record_id, name, email = row

        if (search_input in str(record_id).lower() or
            search_input in (name or "").lower() or
            search_input in (email or "").lower()):
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
            insert_row(tree, row)


def reset_search(query_entry, scope_combo, refresh_fn):
    """
    Resets the search fields and refreshes the tree view.

    :param query_entry: The QLineEdit to clear.
    :type query_entry: QLineEdit
    :param scope_combo: The QComboBox to reset.
    :type scope_combo: QComboBox
    :param refresh_fn: The function to call to refresh the view.
    :type refresh_fn: callable
    """
    query_entry.clear()
    scope_combo.setCurrentIndex(0)
    refresh_fn()


def export_to_csv(tree):
    """
    Exports the data from the tree widget to a CSV file.

    :param tree: The QTreeWidget containing the data.
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
            headers = [tree.headerItem().text(instructor) for instructor in range(tree.columnCount())]
            writer.writerow(headers)

            # Write data
            for instructor in range(top_count):
                item = tree.topLevelItem(instructor)
                row = [item.text(col) for col in range(tree.columnCount())]
                writer.writerow(row)

        QMessageBox.information(tree, "Export Successful", f"Records have been exported to {filename}")
    except Exception as e:
        QMessageBox.critical(tree, "Export Error", f"Failed to export records: {str(e)}")


def open_person_edit_dialog(parent, person, person_type, students, instructors, courses, refresh_fn):
    """
    Opens a dialog to edit a person's (student/instructor) details.

    :param parent: The parent widget.
    :type parent: QWidget
    :param person: The person object to edit.
    :type person: Person
    :param person_type: The type of person ('student' or 'instructor').
    :type person_type: str
    :param students: List of all student objects.
    :type students: list[Student]
    :param instructors: List of all instructor objects.
    :type instructors: list[Instructor]
    :param courses: List of all course objects.
    :type courses: list[Course]
    :param refresh_fn: Callback to refresh the main view.
    :type refresh_fn: callable
    """
    if not person:
        QMessageBox.critical(parent, "Error", "Person not found.")
        return

    dialog = QDialog(parent)
    dialog.setWindowTitle(f"Edit {person_type.title()}")
    dialog.setModal(True)
    dialog.resize(500, 280)

    name_input = QLineEdit(str(person.name))
    age_input = QLineEdit(str(person.age))
    email_input = QLineEdit(person.get_email())
    id_input = QLineEdit(str(getattr(person, f"{person_type}_id")))

    # Layout
    main_frame = QWidget(dialog)
    vbox = QVBoxLayout(main_frame)
    form = QGridLayout()
    form.setContentsMargins(20, 20, 20, 0)
    form.setHorizontalSpacing(10)
    form.setVerticalSpacing(8)

    form.addWidget(QLabel("Name:"), 0, 0)
    form.addWidget(name_input, 0, 1)

    form.addWidget(QLabel("Age:"), 1, 0)
    form.addWidget(age_input, 1, 1)

    form.addWidget(QLabel("Email:"), 2, 0)
    form.addWidget(email_input, 2, 1)

    form.addWidget(QLabel("ID:"), 3, 0)
    form.addWidget(id_input, 3, 1)

    vbox.addLayout(form)

    # Buttons
    button_frame = QWidget(dialog)
    hbox = QHBoxLayout(button_frame)
    hbox.setContentsMargins(20, 20, 20, 20)
    button_save = QPushButton("Save", button_frame)
    button_cancel = QPushButton("Cancel", button_frame)
    hbox.addStretch(1)
    hbox.addWidget(button_cancel)
    hbox.addWidget(button_save)
    vbox.addWidget(button_frame)

    dialog.setLayout(vbox)

    def save_changes():
        name = name_input.text().strip()
        age_str = age_input.text().strip()
        email = email_input.text().strip()
        new_id = id_input.text().strip()

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
            QMessageBox.warning(dialog, "Email Error", str(e))
            return

        setattr(person, id_field, new_id)

        # Update course references if ID changed
        if old_id != new_id:
            if person_type == "student":
                for course in courses:
                    for index, student in enumerate(getattr(course, "enrolled_students", [])):
                        if student is person:
                            course.enrolled_students[index] = person
            else:  # instructor
                for course in courses:
                    if getattr(course, "instructor", None) is person:
                        course.instructor = person

        dialog.accept()
        refresh_fn()

    button_save.clicked.connect(save_changes)
    button_cancel.clicked.connect(dialog.reject)

    dialog.exec_()


def open_course_edit_dialog(parent, course, students, instructors, courses, refresh_fn):
    """
    Opens a dialog to edit a course's details.

    :param parent: The parent widget.
    :type parent: QWidget
    :param course: The course object to edit.
    :type course: Course
    :param students: List of all student objects.
    :type students: list[Student]
    :param instructors: List of all instructor objects.
    :type instructors: list[Instructor]
    :param courses: List of all course objects.
    :type courses: list[Course]
    :param refresh_fn: Callback to refresh the main view.
    :type refresh_fn: callable
    """
    if not course:
        QMessageBox.critical(parent, "Error", "Course not found.")
        return

    dialog = QDialog(parent)
    dialog.setWindowTitle("Edit Course")
    dialog.setModal(True)
    dialog.resize(400, 180)

    id_input = QLineEdit(str(course.course_id))
    name_input = QLineEdit(str(course.course_name))

    main_frame = QWidget(dialog)
    vbox = QVBoxLayout(main_frame)
    form = QGridLayout()
    form.setContentsMargins(20, 20, 20, 0)
    form.setHorizontalSpacing(10)
    form.setVerticalSpacing(8)

    form.addWidget(QLabel("Course ID:"), 0, 0)
    form.addWidget(id_input, 0, 1)

    form.addWidget(QLabel("Course Name:"), 1, 0)
    form.addWidget(name_input, 1, 1)

    vbox.addLayout(form)

    button_frame = QWidget(dialog)
    hbox = QHBoxLayout(button_frame)
    hbox.setContentsMargins(20, 15, 20, 15)
    button_save = QPushButton("Save", button_frame)
    button_cancel = QPushButton("Cancel", button_frame)
    hbox.addStretch(1)
    hbox.addWidget(button_cancel)
    hbox.addWidget(button_save)
    vbox.addWidget(button_frame)

    dialog.setLayout(vbox)

    def save_course():
        old_id = course.course_id
        new_id = id_input.text().strip()
        new_name = name_input.text().strip()

        if not (require(new_id, "Course ID") and require(new_name, "Course Name")):
            return

        if not validate_unique_id(new_id, courses, "course_id", exclude=course):
            return

        course.course_id = new_id
        course.course_name = new_name

        # Update references in student/instructor lists
        if old_id != new_id:
            for student in students:
                for index, course in enumerate(getattr(student, "registered_courses", [])):
                    if course == old_id:
                        student.registered_courses[index] = new_id
            for instructor in instructors:
                for index, course in enumerate(getattr(instructor, "assigned_courses", [])):
                    if course is course:
                        instructor.assigned_courses[index] = course

        dialog.accept()
        refresh_fn()

    button_save.clicked.connect(save_course)
    button_cancel.clicked.connect(dialog.reject)

    dialog.exec_()


def get_selected_row(tree):
    """
    Retrieves the data from the currently selected row in the tree widget.

    :param tree: The QTreeWidget to get the selection from.
    :type tree: QTreeWidget
    :return: A tuple of the selected row's data, or None.
    :rtype: tuple or None
    """
    items = tree.selectedItems()
    if not items:
        return None
    item = items[0]
    return tuple(item.text(index) for index in range(tree.columnCount()))


def edit_selected(tree, parent, students, instructors, courses, refresh_fn):
    """
    Opens the appropriate edit dialog for the selected record.

    :param tree: The QTreeWidget with the selection.
    :type tree: QTreeWidget
    :param parent: The parent widget for the dialog.
    :type parent: QWidget
    :param students: List of all student objects.
    :type students: list[Student]
    :param instructors: List of all instructor objects.
    :type instructors: list[Instructor]
    :param courses: List of all course objects.
    :type courses: list[Course]
    :param refresh_fn: Callback to refresh the main view.
    :type refresh_fn: callable
    """
    selection = tree.selectedItems()
    if not selection:
        QMessageBox.warning(parent, "No Selection", "Please select a record to edit.")
        return

    record_type, record_id, *_ = get_selected_row(tree)

    if record_type == "Student":
        person = next((student for student in students if str(student.student_id) == str(record_id)), None)
        open_person_edit_dialog(parent, person, "student", students, instructors, courses, refresh_fn)
    elif record_type == "Instructor":
        person = next((instructor for instructor in instructors if str(instructor.instructor_id) == str(record_id)), None)
        open_person_edit_dialog(parent, person, "instructor", students, instructors, courses, refresh_fn)
    elif record_type == "Course":
        course = next((course for course in courses if str(course.course_id) == str(record_id)), None)
        open_course_edit_dialog(parent, course, students, instructors, courses, refresh_fn)


def delete_selected(tree, students, instructors, courses, refresh_fn):
    """
    Deletes the selected record after confirmation.

    :param tree: The QTreeWidget with the selection.
    :type tree: QTreeWidget
    :param students: List of all student objects.
    :type students: list[Student]
    :param instructors: List of all instructor objects.
    :type instructors: list[Instructor]
    :param courses: List of all course objects.
    :type courses: list[Course]
    :param refresh_fn: Callback to refresh the main view.
    :type refresh_fn: callable
    """
    selection = tree.selectedItems()
    if not selection:
        QMessageBox.warning(tree, "No Selection", "Please select a record to delete.")
        return

    record_type, record_id, *_ = get_selected_row(tree)

    reply = QMessageBox.question(
        tree, "Confirm Delete",
        f"Are you sure you want to delete {record_type} {record_id}?",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
    if reply != QMessageBox.Yes:
        return

    if record_type == "Student":
        student = next((student for student in students if str(student.student_id) == str(record_id)), None)
        if student:
            # Remove from course enrollments
            for course in courses:
                if student in getattr(course, "enrolled_students", []):
                    course.enrolled_students.remove(student)
            students.remove(student)

    elif record_type == "Instructor":
        instructor = next((instructor for instructor in instructors if str(instructor.instructor_id) == str(record_id)), None)
        if instructor:
            # Remove instructor assignments
            for course in courses:
                if getattr(course, "instructor", None) is instructor:
                    course.instructor = None
            instructors.remove(instructor)

    elif record_type == "Course":
        course = next((course for course in courses if str(course.course_id) == str(record_id)), None)
        if course:
            # Remove from student/instructor lists
            for student in students:
                if course.course_id in getattr(student, "registered_courses", []):
                    student.registered_courses.remove(course.course_id)
            for instructor in instructors:
                if course.course_id in getattr(instructor, "assigned_courses", []):
                    instructor.assigned_courses.remove(course.course_id)
            courses.remove(course)

    refresh_fn()


def save_all(students, instructors, courses):
    """
    Saves all data to their respective JSON files.

    :param students: List of student objects.
    :type students: list[Student]
    :param instructors: List of instructor objects.
    :type instructors: list[Instructor]
    :param courses: List of course objects.
    :type courses: list[Course]
    """
    try:
        DataManager.save_data(STUDENTS_FILE, students, "student_id")
        DataManager.save_data(INSTRUCTORS_FILE, instructors, "instructor_id")
        DataManager.save_data(COURSES_FILE, courses, "course_id")
        QMessageBox.information(None, "Success", "All data has been saved.")
    except Exception as e:
        QMessageBox.critical(None, "Save Error", f"Failed to save data: {str(e)}")


def load_all(students, instructors, courses, refresh_fn):
    """
    Loads all data from JSON files, skipping duplicates.

    :param students: List to populate with student objects.
    :type students: list[Student]
    :param instructors: List to populate with instructor objects.
    :type instructors: list[Instructor]
    :param courses: List to populate with course objects.
    :type courses: list[Course]
    :param refresh_fn: Callback to refresh the main view.
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

        # Build lookup dictionaries for existing records
        existing_students = {student.student_id for student in students}
        existing_instructors = {instructor.instructor_id for instructor in instructors}
        existing_courses = {course.course_id for course in courses}

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
        QMessageBox.information(None, "Success", "Data loaded successfully.")

    except FileNotFoundError:
        QMessageBox.warning(None, "Files Not Found", "One or more data files could not be found.")
    except Exception as e:
        QMessageBox.critical(None, "Load Error", f"Failed to load data: {str(e)}")


def build_records_tab(parent, students, instructors, courses, on_data_change=None):
    """
    Builds the entire records management tab for the PyQt5 UI.

    :param parent: The parent widget.
    :type parent: QWidget
    :param students: List of student objects.
    :type students: list[Student]
    :param instructors: List of instructor objects.
    :type instructors: list[Instructor]
    :param courses: List of course objects.
    :type courses: list[Course]
    :param on_data_change: Optional callback for when data changes.
    :type on_data_change: callable, optional
    :return: A tuple containing the tree widget, refresh function, and the container widget.
    :rtype: tuple(QTreeWidget, callable, QWidget)
    """
    # Search controls
    search_frame = QWidget(parent)
    search_layout = QHBoxLayout(search_frame)
    search_layout.setContentsMargins(10, 8, 10, 8)

    QLabel("Search:").setParent(search_frame)
    lbl_search = QLabel("Search:", search_frame)
    search_layout.addWidget(lbl_search)

    query_entry = QLineEdit(search_frame)
    query_entry.setFixedWidth(240)
    search_layout.addWidget(query_entry)

    scope_combo = QComboBox(search_frame)
    scope_combo.addItems(["All", "Students", "Instructors", "Courses"])
    scope_combo.setCurrentIndex(0)
    scope_combo.setFixedWidth(140)
    search_layout.addWidget(scope_combo)

    button_search = QPushButton("Search", search_frame)
    button_clear = QPushButton("Clear", search_frame)
    search_layout.addWidget(button_search)
    search_layout.addWidget(button_clear)
    search_layout.addStretch(1)

    # Action buttons
    action_frame = QWidget(parent)
    action_layout = QHBoxLayout(action_frame)
    action_layout.setContentsMargins(10, 0, 10, 8)

    button_edit = QPushButton("Edit", action_frame)
    button_delete = QPushButton("Delete", action_frame)
    button_save_all = QPushButton("Save All", action_frame)
    button_load_all = QPushButton("Load All", action_frame)
    button_export = QPushButton("Export to CSV", action_frame)

    for button in (button_edit, button_delete, button_save_all, button_load_all, button_export):
        action_layout.addWidget(button)
    action_layout.addStretch(1)

    # Main table
    tree = QTreeWidget(parent)
    tree.setColumnCount(4)
    tree.setHeaderLabels(["Type", "ID", "Name", "Email"])
    tree.setRootIsDecorated(False)
    tree.setAlternatingRowColors(True)
    tree.setSelectionMode(QTreeWidget.SingleSelection)
    tree.setUniformRowHeights(True)

    tree.setColumnWidth(0, 140)  # Type
    tree.setColumnWidth(1, 140)  # ID
    tree.setColumnWidth(2, 140)  # Name
    tree.setColumnWidth(3, 250)  # Email

    def refresh_function():
        refresh_tree(tree, students, instructors, courses)
        if callable(on_data_change):
            on_data_change()

    button_search.clicked.connect(lambda: apply_search(tree, query_entry, scope_combo, students, instructors, courses))
    button_clear.clicked.connect(lambda: reset_search(query_entry, scope_combo, refresh_function))
    button_edit.clicked.connect(lambda: edit_selected(tree, parent, students, instructors, courses, refresh_function))
    button_delete.clicked.connect(lambda: delete_selected(tree, students, instructors, courses, refresh_function))
    button_save_all.clicked.connect(lambda: save_all(students, instructors, courses))
    button_load_all.clicked.connect(lambda: load_all(students, instructors, courses, refresh_function))
    button_export.clicked.connect(lambda: export_to_csv(tree))

    container = QWidget(parent)
    container_layout = QVBoxLayout(container)
    container_layout.setContentsMargins(0, 0, 0, 0)
    container_layout.addWidget(search_frame)
    container_layout.addWidget(action_frame)
    container_layout.addWidget(tree)

    tree._on_data_change = on_data_change

    return tree, refresh_function, container 
