"""
This module defines the DatabaseManager class for interacting with the SQLite database.
"""
import sqlite3
from datetime import datetime
import os
import shutil
from student import Student
from instructor import Instructor
from course import Course

class DatabaseManager:
    """
    Manages all interactions with the school's SQLite database.

    :param db_name: The name of the database file, defaults to "school.db".
    :type db_name: str, optional
    """
    def __init__(self, db_name="school.db"):
        self.db_name = db_name
        self.create_tables()
        
    def create_tables(self):
        """
        Creates the necessary database tables if they do not already exist.
        This includes tables for students, instructors, courses, and their relationships.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Create Instructors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS instructors (
                instructor_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Create Courses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                course_id TEXT PRIMARY KEY,
                course_name TEXT NOT NULL
            )
        ''')
        
        # Create Student Course Registration table (many-to-many relationship)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_courses (
                student_id TEXT,
                course_id TEXT,
                FOREIGN KEY (student_id) REFERENCES students (student_id),
                FOREIGN KEY (course_id) REFERENCES courses (course_id),
                PRIMARY KEY (student_id, course_id)
            )
        ''')
        
        # Create Instructor Course Assignment table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS instructor_courses (
                instructor_id TEXT,
                course_id TEXT,
                FOREIGN KEY (instructor_id) REFERENCES instructors (instructor_id),
                FOREIGN KEY (course_id) REFERENCES courses (course_id),
                PRIMARY KEY (instructor_id, course_id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def add_student(self, student):
        """
        Adds a new student to the database.

        :param student: The student object to add.
        :type student: Student
        :raises ValueError: If the student already exists or the email is in use.
        """
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO students (student_id, name, age, email)
                VALUES (?, ?, ?, ?)
            ''', (student.student_id, student.name, student.age, student.get_email()))
            conn.commit()
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Student already exists or email is already in use: {str(e)}")
        finally:
            conn.close()

    def get_all_students(self):
        """
        Retrieves all students from the database.

        :return: A list of Student objects.
        :rtype: list[Student]
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students')
        rows = cursor.fetchall()
        conn.close()
        return [Student(row[1], row[2], row[3], row[0]) for row in rows]

    def delete_student(self, student_id):
        """
        Deletes a student from the database by their ID.

        :param student_id: The ID of the student to delete.
        :type student_id: str
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        cursor.execute('DELETE FROM student_courses WHERE student_id = ?', (student_id,))
        conn.commit()
        conn.close()

    def add_instructor(self, instructor):
        """
        Adds a new instructor to the database.

        :param instructor: The instructor object to add.
        :type instructor: Instructor
        :raises ValueError: If the instructor already exists.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO instructors (instructor_id, name, age, email)
                VALUES (?, ?, ?, ?)
            ''', (instructor.instructor_id, instructor.name, instructor.age, instructor.get_email()))
            conn.commit()
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Instructor already exists: {str(e)}")
        finally:
            conn.close()

    def get_all_instructors(self):
        """
        Retrieves all instructors from the database.

        :return: A list of Instructor objects.
        :rtype: list[Instructor]
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM instructors')
        rows = cursor.fetchall()
        conn.close()
        return [Instructor(row[1], row[2], row[3], row[0]) for row in rows]

    def delete_instructor(self, instructor_id):
        """
        Deletes an instructor from the database by their ID.

        :param instructor_id: The ID of the instructor to delete.
        :type instructor_id: str
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM instructors WHERE instructor_id = ?', (instructor_id,))
        cursor.execute('DELETE FROM instructor_courses WHERE instructor_id = ?', (instructor_id,))
        conn.commit()
        conn.close()

    def add_course(self, course):
        """
        Adds a new course to the database.

        :param course: The course object to add.
        :type course: Course
        :raises ValueError: If the course already exists.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO courses (course_id, course_name)
                VALUES (?,?)
            ''', (course.course_id, course.course_name))
            conn.commit()
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Course already exists: {str(e)}")
        finally:
            conn.close()

    def get_all_courses(self):
        """
        Retrieves all courses from the database.

        :return: A list of Course objects.
        :rtype: list[Course]
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses')
        courses = [Course(row[0], row[1]) for row in cursor.fetchall()]
        conn.close()
        return courses

    def delete_course(self, course_id):
        """
        Deletes a course from the database by its ID.

        :param course_id: The ID of the course to delete.
        :type course_id: str
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM courses WHERE course_id = ?', (course_id,))
        cursor.execute('DELETE FROM student_courses WHERE course_id = ?', (course_id,))
        cursor.execute('DELETE FROM instructor_courses WHERE course_id = ?', (course_id,))
        conn.commit()
        conn.close()

    def register_student_course(self, student_id, course_id):
        """
        Registers a student for a course.

        :param student_id: The ID of the student.
        :type student_id: str
        :param course_id: The ID of the course.
        :type course_id: str
        :raises ValueError: If the registration already exists.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO student_courses (student_id, course_id)
                VALUES (?, ?)
            ''', (student_id, course_id))
            conn.commit()
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Registration already exists: {str(e)}")
        finally:
            conn.close()

    def assign_instructor_course(self, instructor_id, course_id):
        """
        Assigns an instructor to a course.

        :param instructor_id: The ID of the instructor.
        :type instructor_id: str
        :param course_id: The ID of the course.
        :type course_id: str
        :raises ValueError: If the assignment already exists.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO instructor_courses (instructor_id, course_id)
                VALUES (?, ?)
            ''', (instructor_id, course_id))
            conn.commit()
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Assignment already exists: {str(e)}")
        finally:
            conn.close()

    def backup_database(self, backup_path=None):
        """
        Creates a backup of the database file.

        If no backup path is provided, a timestamped backup file is created
        in the current directory.

        :param backup_path: The path to save the backup file, defaults to None.
        :type backup_path: str, optional
        :return: A tuple containing a boolean indicating success and a message.
        :rtype: tuple(bool, str)
        """
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_{timestamp}.db"
            
        try:
            shutil.copy2(self.db_name, backup_path)
            return True, f"Database backed up successfully to {backup_path}"
        except Exception as e:
            return False, f"Backup failed: {str(e)}"