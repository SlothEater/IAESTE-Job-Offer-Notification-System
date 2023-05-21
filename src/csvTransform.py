"""
This module provides a class to transform a CSV file containing application data 
to a new CSV file in a different format.

The CSV file should contain the following columns:
- Ref.No: the reference number of the application
- OfferType: the offer type of the application
- ExchangeType: the exchange type of the application
- Country: the country of the application
- Faculty 1: a string of the form "faculty code-faculty name, number-faculty 
name, ...".

The transformed CSV file will contain the following columns:
- ReferenceNumber: the reference number of the application
- OfferType: the offer type of the application
- ExchangeType: the exchange type of the application
- Country: the country of the application
- FacultyCode: a list of the faculty codes
- FacultyText: a list of the faculty names corresponding to the faculty codes

This module can also delete the original CSV file if specified.

"""
import pandas as pd
import json
import re
import os
from src.constants.paths import INPUT_CSV_FILE_PATH, TRANSFORMED_CSV_FILE_PATH


class TransformCSV:

    def __init__(self):
        """
        Initialize the TransformCSV class with the input and output CSV file 
        paths.
        """
        self.input_csv_file_path = INPUT_CSV_FILE_PATH
        self.output_csv_file_path = TRANSFORMED_CSV_FILE_PATH

    def _splitFacultyString(self, faculty_string):
        """
        Split the faculty string into a list of faculty codes and names.

        Args:
        - faculty_string (str): a string of the form "faculty code-faculty name, 
        number-faculty name, ..."

        Returns:
        - (list): a list of strings of the form ["faculty code", "faculty name", 
        ...]
        """
        faculty_list = re.split(r'(,\s+\d+)', faculty_string)
        return (faculty_list[:1] + [
            faculty_list[i][2:] + faculty_list[i + 1]
            for i in range(1,
                           len(faculty_list) - 1, 2)
        ])

    def _separateFacultyValues(self, faculty_values):
        """
        Separate faculty codes and names into separate lists.

        Args:
        - faculty_values (list): a list of strings of the form ["faculty code", 
        "faculty name", ...]

        Returns:
        - (tuple): a tuple of two lists of strings - (faculty_codes, 
        faculty_names)
        """
        return zip(*[item.split('-', 1) for item in faculty_values])

    def getTransformedCSV(self, delete_Source=False):
        """
        Transform the CSV file and return the resulting pandas dataframe.

        Args:
        - delete_Source (bool): whether or not to delete the original CSV file 
        (default: False)

        Returns:
        - (pandas.DataFrame): the resulting transformed dataframe
        """
        # Load CSV file into a pandas dataframe
        df = pd.read_csv(self.input_csv_file_path)

        # Keep only the required columns
        df = df[[
            'Ref.No', 'OfferType', 'ExchangeType', 'Country', 'Faculty 1'
        ]]
        df.rename(columns={'Ref.No': 'ReferenceNumber'}, inplace=True)

        # Split the 'Faculty 1' column into a list of faculties
        df['Faculty 1'] = df['Faculty 1'].apply(self._splitFacultyString)

        # Apply separateFacultyValues to the Faculty 1 column
        df[['FacultyCode', 'FacultyText']] = pd.DataFrame(
            df['Faculty 1'].apply(self._separateFacultyValues).tolist(),
            index=df.index)

        # Drop the original Faculty 1 column
        df = df.drop('Faculty 1', axis=1)

        # Keep only records with ExchangeType: ['COBE', 'FCFS'] and OfferType:
        # ['OPEN']
        df = df[df['ExchangeType'].isin(['COBE', 'FCFS'])
                & df['OfferType'].isin(['OPEN'])]

        # Delete the original file if delete_Source
        if delete_Source: os.remove(self.input_csv_file_path)

        # Return the dataframe
        return df
