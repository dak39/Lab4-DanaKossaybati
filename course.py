"""
This module defines the Course class.
"""
from instructor import Instructor
from student import Student

class Course:
    """
    Represents a school course.

    :param course_id: The unique identifier for the course.
    :type course_id: str
    :param course_name: The name of the course.
    :type course_name: str
    :param instructor: The instructor for the course, defaults to None.
    :type instructor: Instructor, optional
    :param enrolled_students: A list of students enrolled in the course, defaults to None.
    :type enrolled_students: list[Student], optional
    """
    def __init__(self, course_id: str, course_name: str, instructor: Instructor = None, enrolled_students = None):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = None
        if enrolled_students is None:
            self.enrolled_students = []
        else:
            self.enrolled_students = enrolled_students
        
    def add_instructor(self, instructor):
        """
        Assigns an instructor to the course.

        :param instructor: The instructor to assign.
        :type instructor: Instructor
        :raises ValueError: If the provided object is not an instance of Instructor.
        """
        if not isinstance(instructor, Instructor):
            raise ValueError("Only an Instructor can be assigned to the course.")
        self.instructor = instructor

    def add_student(self, student):
        """
        Enrolls a student in the course.

        If the student is already enrolled, this method does nothing.

        :param student: The student to enroll.
        :type student: Student
        :raises ValueError: If the provided object is not an instance of Student.
        """
        if not isinstance(student, Student):
            raise ValueError("Only a Student can be enrolled in the course.")
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
        
    def to_dict(self):
        """
        Converts the Course object to a dictionary for serialization.

        :return: A dictionary representation of the course.
        :rtype: dict
        """
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            "instructor": self.instructor.to_dict() if self.instructor is not None else None,
            'enrolled_students': [student.to_dict() for student in self.enrolled_students] 
        }
        
    @classmethod
    def from_dict(cls, data):
        """
        Creates a Course object from a dictionary.

        :param data: A dictionary containing course data.
        :type data: dict
        :return: A new Course object.
        :rtype: Course
        """
        instructor = Instructor.from_dict(data.get('instructor')) if data.get('instructor') else None
        students = [Student.from_dict(student_data) for student_data in data['enrolled_students']]
        return cls(data['course_id'], data['course_name'], instructor, students)

    def display_course(self):
        """
        Generates a human-readable string for the course object.

        :return: A formatted string with the course's ID and name.
        :rtype: str
        """
        return f"{self.course_id} - {self.course_name}"