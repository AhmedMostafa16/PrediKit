from typing import Self

from pandas import DataFrame

from predikit.errors import DataNotFittedError

from .._typing import (
    MergeHow,
    NaPosition,
    SortKind,
)
from ..preprocessing._base import BasePreprocessor
from ._misc_base import RowSelectionInterpreter


class RowSelector(BasePreprocessor):
    """A class used to select rows from a DataFrame based on the input string.

    Attributes
    ----------
    input : str
        The special form input string to interpret.

    Examples
    --------
    >>> import predikit as pk
    >>> from pandas import DataFrame
    >>> data = pd.DataFrame({'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    >>> input = '''
    ... -2
    ... 5-7
    ... 8+
    ... '''
    >>> rs = pk.RowSelector(input)
    >>> rs.fit_transform(data)
    """

    def __init__(
        self,
        input: str,
        zero_indexed: bool = False,
    ) -> None:
        self.input: str = input
        self.zero_indexed: bool = zero_indexed

    def fit(self, data: DataFrame, columns: list[str] | None = None) -> Self:
        if columns:
            data = data[columns]

        if not self.input:
            raise ValueError("Input String for Row Selection is Empty")

        interpreter = RowSelectionInterpreter(
            self.input, len(data), zero_indexed=self.zero_indexed
        )

        self.selection = interpreter.interpret()

        return self

    def transform(
        self, data: DataFrame, columns: list[str] | None = None
    ) -> DataFrame:
        if columns:
            data = data[columns]

        if not hasattr(self, "selection"):
            raise DataNotFittedError(
                "Data must be fitted first using the 'fit' method"
            )

        if not self.zero_indexed:
            data.index += 1

        return data.iloc[self.selection]


class RowIdentifier(BasePreprocessor):
    """A class used to add a new column to a DataFrame with unique identifiers.

    Attributes
    ----------
    new_col_name : str
        The name of the new column to add that will contain each row id.
        >>> `id`
    value_prefix : str
        A prefix to add to the unique identifier of each row.
        >>> `row_`1
    start_value : int
        The starting value of the unique identifier.
        >>> `1`
    from_exisiting_col : str
        Use an existing column as the unique identifier of each row and
        generate a new id column based on the values of that existing column.
        >>> `SSN`
    """

    def __init__(
        self,
        new_col_name: str = "id",
        *,
        value_prefix: str = "",
        start_value: int = 0,
        from_exisiting_col: str | None = None,
    ) -> None:
        self.name: str = new_col_name
        self.prefix: str = value_prefix
        self.start: int = start_value
        self.existing_col: str | None = from_exisiting_col

    def fit(self, data: DataFrame, columns: list[str] | None = None) -> Self:
        if columns:
            data = data[columns]

        if self.existing_col:
            self.indices = data[self.existing_col]
        else:
            self.indices = self.start + data.reset_index().index

            if self.prefix:
                self.indices = self.prefix + self.indices.astype(str)

        return self

    def transform(
        self, data: DataFrame, columns: list[str] | None = None
    ) -> DataFrame:
        if columns:
            data = data[columns]

        if not hasattr(self, "indices"):
            raise DataNotFittedError(
                "Data must be fitted first using the 'fit' method"
            )

        data[self.name] = self.indices

        return data


class Sorter(BasePreprocessor):
    """A class used to sort a DataFrame based on the input string.

    Attributes
    ----------
    by : str | list[str]
        The column or columns to sort by.
    ascending : bool
        Whether to sort in ascending order.
    kind : SortKind
        The sorting algorithm to use.
    na_position : NaPosition
        Where to place NaN values in the sorted DataFrame.
    """

    def __init__(
        self,
        by: str | list[str],
        ascending: bool = True,
        kind: SortKind = "quicksort",
        na_position: NaPosition = "last",
    ) -> None:
        self.by: str | list[str] = by
        self.ascending: bool = ascending
        self.kind: SortKind = kind
        self.na_position: NaPosition = na_position

    def transform(
        self, data: DataFrame, columns: list[str] | None = None
    ) -> DataFrame:
        if columns:
            data = data[columns]

        return data.sort_values(
            by=self.by,
            ascending=self.ascending,
            kind=self.kind,
            na_position=self.na_position,
        )


class Merger(BasePreprocessor):
    """A class used to merge two DataFrames.
    Attributes
    ----------
    data : DataFrame
        The DataFrame to merge with.
    on : str | list[str]
        The column or columns to merge on.
    how : MergeHow
        The type of merge to perform.
    suffixes : tuple[str, str]
        The suffixes to add to the column names if they are the same in both
        DataFrames.
    """

    def __init__(
        self,
        data: DataFrame,
        on: str | list[str],
        how: MergeHow = "inner",
        suffixes: tuple[str, str] = ("_x", "_y"),
    ) -> None:
        self.data: DataFrame = data
        self.on: str | list[str] = on
        self.how: MergeHow = how
        self.suffixes: tuple[str, str] = suffixes

    def transform(
        self, data: DataFrame, columns: list[str] | None = None
    ) -> DataFrame:
        if columns:
            data = data[columns]

        # catch KeyError if `on` attribute column is not found
        return data.merge(
            right=self.data,
            on=self.on,
            how=self.how,
            suffixes=self.suffixes,
        )
