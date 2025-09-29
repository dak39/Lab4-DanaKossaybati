"""
This module defines the Instructor class, a subclass of Person.
"""
from person import Person

class Instructor(Person):
    """
    Represents an instructor, inheriting from the Person class.

    :param name: The name of the instructor.
    :type name: str
    :param age: The age of the instructor.
    :type age: int
    :param email: The email address of the instructor.
    :type email: str
    :param instructor_id: The unique identifier for the instructor.
    :type instructor_id: str
    :param assigned_courses: A list of course IDs assigned to the instructor, defaults to None.
    :type assigned_courses: list[str], optional
    """
    def __init__(self, name: str, age: int, email: str, instructor_id: str, assigned_courses = None):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        if assigned_courses is None:
            self.assigned_courses = []
        else:
            self.assigned_courses = assigned_courses

    def assign_course(self, course):
        """
        Assigns a course to the instructor.

        If the course is already assigned, this method does nothing.

        :param course: The course to assign.
        :type course: Course
        """
        if course.course_id not in self.assigned_courses:
            self.assigned_courses.append(course.course_id)
        
    def to_dict(self):
        """
        Converts the Instructor object to a dictionary for serialization.

        :return: A dictionary representation of the instructor.
        :rtype: dict
        """
        data = super().to_dict()
        data.update({
            "instructor_id": self.instructor_id,
            "assigned_courses": self.assigned_courses
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """
        Creates an Instructor object from a dictionary.

        :param data: A dictionary containing instructor data.
        :type data: dict
        :return: A new Instructor object.
        :rtype: Instructor
        """
        try:
            name = Person.validate_name(data.get("name", ""))
            age = Person.validate_age(data.get("age", 0))
            email = Person.validate_email(data.get("email", ""))
            instructor_id = data["instructor_id"]
            assigned_courses = data.get("assigned_courses", [])
        except Exception:
            pass
        return cls(name, age, email, instructor_id, assigned_courses)
    
    def display_instructor(self): 
        """
        Generates a human-readable string for the instructor object.

        :return: A formatted string with the instructor's ID and name.
        :rtype: str
        """
        return f"{self.instructor_id} - {self.name}"
