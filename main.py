from src.websiteScraper import ForeignOffersExtractor
from src.csvTransform import TransformCSV
from src.csvLoadAndCompare import LoadAndCompare
from src.constants.relevantFacultyCodes import RELEVANT_FACULTY_CODES
from src.botHandler import send_message

import pandas as pd
import numpy as np
import time
import datetime


def getOutputString(data):
    """
    Create output string to send in the message

    Args:
        data (tuple): A tuple containing two pandas DataFrame objects

    Returns:
        str: The output string
    """
    df_new, df_missing = data

    faculty_codes = list(RELEVANT_FACULTY_CODES.values())

    # Split the FacultyCode list into separate rows
    def checkIfNone(entry):
        if entry == None: return ['Nan']
        return entry

    df_new['FacultyText'] = df_new['FacultyText'].apply(checkIfNone)
    df_new = df_new.explode(['FacultyCode', 'FacultyText'])

    if df_new.empty:
        output_string = "No new offers.\n"
    else:
        # Filter rows that match the list of values
        def filter_relevant_faculty_code(x):
            if x in faculty_codes: return True
            return False

        df_new['to_keep'] = df_new['FacultyCode'].apply(
            filter_relevant_faculty_code)
        relevant_new_records = df_new[df_new['to_keep']]

        # Group the dataframe by the exploded FacultyCode column and aggregate 
        # ReferenceNumber into a list for each group
        grouped = relevant_new_records.groupby(
            'FacultyCode')['ReferenceNumber'].agg(list)

        # Create output string for each group
        output_strings = []
        for group_name, ref_numbers in grouped.items():
            output_strings.append(
                (f"New available offers for {group_name}-"
                f"{next((k for k, v in RELEVANT_FACULTY_CODES.items() if v == group_name), None)}:"
                f" {ref_numbers}\n")
            )
        output_string = "\n".join(output_strings)

    if df_missing.empty:
        output_string += "\nNo jobs have become unavailable."
    else:
        # Filter rows that match the list of values
        old_mask = df_new['FacultyCode'].apply(
            lambda x: any([i for i in faculty_codes if i in x]))
        relevant_old_records = df_missing[old_mask]
        output_string += ("\nNo longer available: "
        f"{relevant_old_records['ReferenceNumber'].tolist()}")

    return output_string


def main():
    """
    The main function that runs the whole process
    """
    print('Scraping CSV')
    getCSVData = ForeignOffersExtractor()
    getCSVData.getCSV()

    print('Transforming CSV')
    getNewCSVData = TransformCSV()
    newCSVData = getNewCSVData.getTransformedCSV(True)

    print('Sending Message')
    dataVerifier = LoadAndCompare(newCSVData)
    data = dataVerifier.verifyData()

    if data == None:
        output_string = getOutputString((newCSVData, pd.DataFrame()))
        send_message(output_string)
    else:
        output_string = getOutputString(data)
        send_message(output_string)


if __name__ == '__main__':
    try:
        main()
    except:
        send_message('System crashed!')
