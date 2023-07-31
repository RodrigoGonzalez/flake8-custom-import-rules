""" A basic module. """
from datetime import datetime
from uuid import UUID
from uuid import uuid4

import numpy as np
import pandas as pd
from attrs import define, field


@define(slots=True)
class Y:
    """A basic class"""

    _id: UUID | None = field(factory=uuid4)
    _name: str | None = field(default="name")
    _description: str | None = field(default="description")
    _created_at: datetime | None = field(factory=datetime.now)

    def id(self):
        """Get the id."""
        return self._id

    def name(self):
        """Get the name."""
        return self._name

    def description(self):
        """Get the description."""
        return self._description

    def created_at(self):
        """Get the created_at."""
        return self._created_at

    @staticmethod
    def get_shape(df: pd.DataFrame) -> tuple[int, int]:
        """
        Returns the number of rows and columns of the dataset.

        Parameters
        ----------
        df

        Returns
        -------
        tuple(int, int)
            A tuple with the number of rows and columns of the dataset.
        """
        return df.shape

    @staticmethod
    def get_columns(df: pd.DataFrame) -> list[str]:
        """
        Returns a list of the dataset's column names.

        Parameters
        ----------
        df

        Returns
        -------

        """
        return df.columns.tolist()

    @staticmethod
    def get_dtypes(df: pd.DataFrame) -> dict[str, str]:
        """
        Returns a dictionary with column names as keys and their data types as values.

        Parameters
        ----------
        df

        Returns
        -------

        """
        return df.dtypes.to_dict()

    @staticmethod
    def get_missing_values(df: pd.DataFrame) -> dict[str, int]:
        """
        Returns a dictionary with column names as keys and the number of missing
        values in each column as values.

        Parameters
        ----------
        df

        Returns
        -------

        """
        return df.isna().sum().to_dict()

    @staticmethod
    def get_unique_values(df: pd.DataFrame) -> dict[str, int]:
        """
        Returns a dictionary with column names as keys and the number of unique
        values in each column as values.

        Parameters
        ----------
        df

        Returns
        -------

        """
        return df.nunique().to_dict()

    @staticmethod
    def get_descriptive_statistics(
            df: pd.DataFrame, columns: list[str] | None = None,
    ) -> pd.DataFrame:
        """Returns a DataFrame with descriptive statistics
        (count, mean, median, standard deviation, min, max, etc.)
        for the specified columns or all numeric columns if no columns are provided.
        """
        if columns is None:
            columns = df.select_dtypes(include=np.number).columns.tolist()
        return df[columns].describe().T

    @staticmethod
    def get_value_counts(df: pd.DataFrame, column: str, normalize: bool = False) -> pd.Series:
        """

        Parameters
        ----------
        df
        column
        normalize

        Returns
        -------

        """
        return df[column].value_counts(normalize=normalize)

    def describe(self, df: pd.DataFrame, include: str | list[str] | None = None) -> pd.DataFrame:
        """
        Returns a DataFrame with a summary of the dataset, including shape, data types,
        missing values, unique values, and descriptive statistics.

        The include parameter can be used to specify which data types to consider
        (e.g., 'all', 'number', 'object', etc.) or a list of specific column names.
        """
        if include and include != "all":
            df = df.select_dtypes(include=include)

        shape = self.get_shape(df)
        columns = self.get_columns(df)
        dtypes = self.get_dtypes(df)
        missing_values = self.get_missing_values(df)
        unique_values = self.get_unique_values(df)
        descriptive_statistics = self.get_descriptive_statistics(df, columns)

        return pd.DataFrame(
            {
                "shape": [shape],
                "columns": [columns],
                "dtypes": [dtypes],
                "missing_values": [missing_values],
                "unique_values": [unique_values],
                "descriptive_statistics": [descriptive_statistics],
            }
        )
