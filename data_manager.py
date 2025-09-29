"""
This module provides a DataManager class for handling JSON data storage.
"""
import json

class DataManager:
    """
    A manager for saving and loading data to and from JSON files.
    """
    
    @staticmethod
    def save_data(filename, data, key_field):
        """
        Saves a list of records to a JSON file, updating existing records
        and adding new ones.

        :param filename: The path to the JSON file.
        :type filename: str
        :param data: A list of objects to save. Each object must have a 'to_dict' method.
        :type data: list
        :param key_field: The name of the unique key field used to identify records.
        :type key_field: str
        """
        
        try:
            with open(filename, "r", encoding="utf-8") as f:
                existing = json.load(f)
                if not isinstance(existing, list):
                    existing = []
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []

        
        by_key = {str(record[key_field]): record for record in existing if isinstance(record, dict) and key_field in record}

        for obj in data or []:
            if obj is None:
                continue
            record = obj.to_dict()
            key = str(record.get(key_field))
            if not key:
                continue
            by_key[key] = {**by_key.get(key, {}), **record}

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(list(by_key.values()), f, indent=4, ensure_ascii=False)

    @staticmethod
    def overwrite_json_file(filename, data):
        """
        Overwrites a JSON file with new data.

        :param filename: The path to the JSON file.
        :type filename: str
        :param data: The data to write to the file.
        :type data: any
        """
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_json(filename):
        """
        Loads data from a JSON file.

        :param filename: The path to the JSON file.
        :type filename: str
        :return: The data loaded from the file.
        :rtype: any
        """
        
        with open(filename, 'r') as file:
            return json.load(file)
