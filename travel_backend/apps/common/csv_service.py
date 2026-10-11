import pandas as pd

from rest_framework import status
from rest_framework.response import Response
import pandas as pd


class CSVService:
    @staticmethod
    def read_csv(file):
        return pd.read_csv(file)

    @staticmethod
    def validate_columns(dataframe, required_columns):
        missing_columns = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        return missing_columns