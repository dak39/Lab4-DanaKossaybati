"""
This module provides validation functions for the application's forms.
"""
from tkinter import messagebox
from person import Person

def validate_name(name):
    """
    Validates a name using Person.validate_name and shows a warning on failure.

    :param name: The name to validate.
    :type name: str
    :return: True if the name is valid, False otherwise.
    :rtype: bool
    """
    try:
        Person.validate_name(name)
        return True
    except ValueError as e:
        messagebox.showwarning("Invalid Input", str(e))
        return False
        
def validate_age(age_str):
    """
    Validates an age string using Person.validate_age and shows a warning on failure.

    :param age_str: The age string to validate.
    :type age_str: str
    :return: True if the age is valid, False otherwise.
    :rtype: bool
    """
    try:
        Person.validate_age(age_str)
        return True
    except ValueError as e:
        messagebox.showwarning("Invalid Input", str(e))
        return False
     
def validate_email(email):
    """
    Validates an email using Person.validate_email and shows a warning on failure.

    :param email: The email to validate.
    :type email: str
    :return: True if the email is valid, False otherwise.
    :rtype: bool
    """
    try:
        Person.validate_email(email)
        return True
    except ValueError as e:
        messagebox.showwarning("Invalid Input", str(e))
        return False

def require(value, label):
    """
    Checks that a value is not empty and shows a warning if it is.

    :param value: The value to check.
    :type value: any
    :param label: The label for the value, used in the warning message.
    :type label: str
    :return: True if the value is not empty, False otherwise.
    :rtype: bool
    """
    if not value:
        messagebox.showwarning("Invalid Input", f"{label} cannot be empty.")
        return False
    return True

def validate_unique_id(new_id, items, attr_name, exclude=None):
    """
    Validates that a given ID is unique among a list of objects.

    :param new_id: The new ID to validate.
    :type new_id: str
    :param items: A list of objects to check for uniqueness against.
    :type items: list
    :param attr_name: The name of the ID attribute on the objects.
    :type attr_name: str
    :param exclude: An optional object to exclude from the uniqueness check, defaults to None.
    :type exclude: any, optional
    :return: True if the ID is unique, False otherwise.
    :rtype: bool
    """
    new_id = str(new_id).strip()
    for obj in items:
        if str(getattr(obj, attr_name)) == new_id and obj is not exclude:
            messagebox.showwarning("Invalid Input", f"{attr_name.replace('_', ' ').title()} must be unique.")
            return False
    return True
