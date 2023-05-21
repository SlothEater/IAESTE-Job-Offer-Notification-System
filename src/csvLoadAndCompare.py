import pandas as pd
import os
from src.constants.paths import TRANSFORMED_CSV_FILE_PATH


class LoadAndCompare:
    """
    A class for loading and comparing CSV data.

    Args:
        newCSVData (pandas.DataFrame): The new CSV data to compare against.

    Attributes:
        new_data (pandas.DataFrame): The new CSV data.
    """

    def __init__(self, newCSVData):
        self.new_data = newCSVData

    def _loadHistoricalData(self):
        """
        Loads the historical CSV data.

        Returns:
            pandas.DataFrame: The historical CSV data.
        """
        return pd.read_csv(TRANSFORMED_CSV_FILE_PATH)

    def _checkIfExists(self):
        """
        Checks if the historical CSV data file exists.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return os.path.exists(TRANSFORMED_CSV_FILE_PATH)

    def _saveNewData(self):
        """
        Saves the new CSV data to the file system.
        """
        self.new_data.to_csv(TRANSFORMED_CSV_FILE_PATH, index=False)

    def _compareData(self, historical_data):
        """
        Compares the new CSV data to the historical CSV data.

        Args:
            historical_data (pandas.DataFrame): The historical CSV data to 
            compare against.

        Returns:
            Tuple(pandas.DataFrame, pandas.DataFrame): A tuple containing two 
            DataFrames: the new data that was not found in the historical data, 
            and the historical data that was missing in the new data.
        """
        # merging dataframes by ReferenceNumber.No with outer join
        merged_df = pd.merge(self.new_data,
                             historical_data,
                             on='ReferenceNumber',
                             how='outer',
                             suffixes=('_DF1', '_DF2'))

        # Save the dataframe as a CSV file
        self._saveNewData()

        # selecting rows which are not in both datasets
        df_new = merged_df[merged_df['FacultyCode_DF2'].isna()]
        df_missing = merged_df[merged_df['FacultyCode_DF1'].isna()]

        df_new = self.new_data[self.new_data['ReferenceNumber'].isin(
            df_new['ReferenceNumber'].tolist())]
        df_missing = historical_data[historical_data['ReferenceNumber'].isin(
            df_new['ReferenceNumber'].tolist())]

        return df_new, df_missing

    def verifyData(self):
        """
        Verifies the new CSV data against the historical CSV data.

        Returns:
            Tuple(pandas.DataFrame, pandas.DataFrame): A tuple containing two 
            DataFrames: the new data that was not found in the historical data, 
            and the historical data that was missing in the new data.
        """
        if not self._checkIfExists():
            print('No Historical data found, saving new data')
            self._saveNewData()
            return None
        historical_data = self._loadHistoricalData()
        return (self._compareData(historical_data))
