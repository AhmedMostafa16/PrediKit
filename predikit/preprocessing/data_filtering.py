import logging
from typing import (
    Self,
    cast,
)

from pandas import DataFrame

from ._base import (
    BasePreprocessor,
    FilterOperator,
)


class DataFilteringProcessor(BasePreprocessor):
    """
    A class used to filter data based on a specified operator and value.

    Attributes
    ----------
    operator : FilterOperator
        The operator to use for filtering.
    value : str, optional
        The value to use for filtering.
    case_sensitive : bool
        Whether the filtering should be case sensitive.
    verbose : bool
        Whether to log the filtering process.
    """

    def __init__(
        self,
        operator: FilterOperator | str,
        value: str | None = None,
        case_sensitive: bool = True,
        verbose: bool = False,
    ) -> None:
        self.operator = operator
        self.value = value
        self.case_sensitive = case_sensitive
        self.verbose = verbose

    def fit(self, data: DataFrame, column: str | None = None) -> Self:
        """
        Compute the necessary parameters for filtering.

        Parameters
        ----------
        data : DataFrame
            The data to be filtered.
        column : str, optional
            The column to be filtered.

        Returns
        -------
        BasicFilteringProcessor
            The instance itself.
        """
        if isinstance(self.operator, str):
            self.operator = FilterOperator.from_str(self.operator)

        if not column:
            raise ValueError("Column name must be provided")

        self._numeric = self._is_numeric(data, column)
        self._query = self._parse_query(column, self.operator, self.value)
        return self

    @override
    def transform(
        self, data: DataFrame, column: str | None = None
    ) -> DataFrame:
        """
        Apply the filtering to the data.

        Parameters
        ----------
        data : DataFrame
            The data to be filtered.
        column : str, optional
            This parameter is kept for codebase consistency but should always
            be None in this context.

        Returns
        -------
        DataFrame
            The filtered data.
        """
        if not hasattr(self, "_query"):
            raise ValueError(
                "Data must be fitted first using the 'fit' method"
            )

        self.operator = cast(FilterOperator, self.operator)

        if self.verbose:
            logging.debug(f"Filtering data by => [{self._query}]")

        if self.operator.is_containment_operator and self._numeric:
            data = data.astype(str)

        data = data.query(self._query)

        return data

    def _parse_query(
        self,
        column: str,
        operator: FilterOperator,
        value: str | None = None,
    ) -> str:
        """
        Generate the query string based on the operator and value.

        Parameters
        ----------
        column : str
            The column to be filtered.
        operator : FilterOperator
            The operator to use for filtering.
        value : str, optional
            The value to use for filtering.

        Returns
        -------
        str
            The query string.
        """
        if operator.is_comparison_operator:
            return f"`{column}` {operator.to_str} {value}"

        if operator.is_nullity_operator:
            return f"`{column}`.{operator.to_str}"

        if operator.is_containment_operator:
            negator = (
                "~" if operator == FilterOperator.DOES_NOT_CONTAIN else ""
            )

            return "{0}`{1}`.str.contains('{2}', case={3})".format(
                negator, column, value, self.case_sensitive
            )

        raise ValueError(f"Invalid operator: {operator}")

    @staticmethod
    def _is_numeric(data: DataFrame, column: str) -> bool:
        """
        Check if the column is numeric.

        Parameters
        ----------
        data : DataFrame
            The data to be checked.
        column : str
            The column to be checked.

        Returns
        -------
        bool
            True if the column is numeric, False otherwise.
        """
        return data[column].dtype.kind in "biufc"
