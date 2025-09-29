"""
This module defines the Student class, a subclass of Person.
"""
from person import Person

class Student(Person):
    """
    Represents a student, inheriting from the Person class.

    :param name: The name of the student.
    :type name: str
    :param age: The age of the student.
    :type age: int
    :param email: The email address of the student.
    :type email: str
    :param student_id: The unique identifier for the student.
    :type student_id: str
    :param registered_courses: A list of course IDs the student is registered for, defaults to None.
    :type registered_courses: list[str], optional
    """
    def __init__(self, name: str, age: int, email: str, student_id: str, registered_courses = None):
        super().__init__(name, age, email)
        self.student_id = student_id
        if registered_courses is None:
            self.registered_courses = []
        else:
            self.registered_courses = registered_courses

    def register_course(self, course):
        """
        Registers a student for a course.

        If the student is already registered for the course, this method does nothing.

        :param course: The course to register for.
        :type course: Course
        """
        if course.course_id not in self.registered_courses:
            self.registered_courses.append(course.course_id)

    def to_dict(self):
        """
        Converts the Student object to a dictionary for serialization.

        :return: A dictionary representation of the student.
        :rtype: dict
        """
        data = super().to_dict()
        data.update({
            "student_id": self.student_id,
            "registered_courses": self.registered_courses
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """
        Creates a Student object from a dictionary.

        :param data: A dictionary containing student data.
        :type data: dict
        :return: A new Student object.
        :rtype: Student
        """
        try:
            if(name := data.get("name")) is None:
                raise ValueError("Name is required")
            if(age := data.get("age")) is None:
                raise ValueError("Age is required")
            if(email := data.get("email")) is None:
                raise ValueError("Email is required")
            if(student_id := data.get("student_id")) is None:
                raise ValueError("Student ID is required")
            name = Person.validate_name(data.get("name"))
            age = Person.validate_age(data.get("age", 1))
            email = Person.validate_email(data.get("email", ""))
            student_id = data["student_id"]
            registered_courses = data.get("registered_courses", [])
        except Exception:
            pass
        return cls(name, age, email, student_id, registered_courses)
    
    def display_student(self):
        """
        Generates a human-readable string for the student object.

        :return: A formatted string with the student's ID and name.
        :rtype: str
        """
        return f"{self.student_id} - {self.name}"