"""
This module defines the base Person class.
"""
import re

class Person:
    """
    Represents a person with a name, age, and email address.

    :param name: The name of the person.
    :type name: str
    :param age: The age of the person.
    :type age: int
    :param email: The email address of the person.
    :type email: str
    """
    def __init__(self, name: str, age: int, email: str):
        self.name = name.strip()
        self.age = self.validate_age(age)
        self._email = self.validate_email(email)
        
    @staticmethod
    def validate_name(name):
        """
        Validates that a name is not empty and contains only alphabetic characters.

        :param name: The name to validate.
        :type name: str
        :raises ValueError: If the name is empty or not alphabetic.
        :return: The validated name.
        :rtype: str
        """
        if not name:
            raise ValueError("Name cannot be empty")
        if not name.isalpha():
            raise ValueError("Name must be alphabetic.")
        return name.strip()

    @staticmethod
    def validate_email(email):
        """
        Validates an email address using a regular expression.

        :param email: The email address to validate.
        :type email: str
        :raises ValueError: If the email format is invalid.
        :return: The validated email address.
        :rtype: str
        """
        if not email:
            raise ValueError("Email cannot be empty")
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if re.match(pattern, email):
            return email
        raise ValueError("Invalid email format")

    @staticmethod
    def validate_age(age):
        """
        Validates that an age is an integer between 1 and 120.

        :param age: The age to validate.
        :type age: int
        :raises ValueError: If the age is not a valid number or is out of range.
        :return: The validated age as an integer.
        :rtype: int
        """
        if age is None:
            raise ValueError("Age cannot be empty")
        try:
            age_int = int(age)
        except (TypeError, ValueError):
            raise ValueError("Age must be a number.")
        if not (1 <= age_int <= 120):
            raise ValueError("Age must be between 1 and 120.")
        return age_int

    def introduce(self):
        """
        Prints a simple introduction for the person.
        """
        print("Hey, I'm " + self.name + ", and I'm " + str(self.age) + " years old.")
        
    def get_email(self):
        """
        Gets the person's email address.

        :return: The email address.
        :rtype: str
        """
        return self._email
    
    def set_email(self, new_email):
        """
        Sets the person's email address after validation.

        :param new_email: The new email address.
        :type new_email: str
        """
        self._email = self.validate_email(new_email)
        
    def to_dict(self):
        """
        Converts the Person object to a dictionary for serialization.

        :return: A dictionary representation of the person.
        :rtype: dict
        """
        return {
            "name": self.name,
            "age": self.age,
            "email": self._email
        }

    @classmethod
    def from_dict(cls, d):
        """
        Creates a Person object from a dictionary.

        :param d: A dictionary containing person data.
        :type d: dict
        :return: A new Person object.
        :rtype: Person
        """
        return cls(
            name=d["name"],
            age=int(d["age"]),
            email=d.get("email", "")
        )
        