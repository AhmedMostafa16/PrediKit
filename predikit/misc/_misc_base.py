from enum import (
    Enum,
    auto,
)
from typing import Callable


class SelectionForm(Enum):
    """The selection form of the Row Selection Interpreter.

    Attributes
    ----------
    SINGLE : enum member
        A single digit returns only the entered row.
        >>> 5
    RANGE : enum member
        A range of numbers returns the rows in the range,
        including the entered rows.
        >>> 17-20
    TO : enum member
        A minus sign before a number returns first through the entered row.
        >>> -2
    FROM : enum member
        A number followed by a plus sign returns the entered row through the
        last row.
        >>> 5+
    """

    SINGLE = auto()
    RANGE = auto()
    TO = auto()
    FROM = auto()


class RowSelectionInterpreter:
    """
    Interpreting the input digits and signs to Row Selector Node

    Ranges to Return: Enter the rows or range of rows to return.

    A single digit returns only the entered row.
    For example, 3 returns only row 3.

    A minus sign before a number returns row 1 through the entered row.
    For example, -2 returns rows 1 and 2.

    A range of numbers returns the rows in the range,
    including the entered rows.
    For example, 17-20 returns rows 17, 18, 19, and 20.

    A number followed by a plus sign returns the entered row through the
    last row. For example, 50+ returns row 50 through the last row.

    Any combination can be used at the same time by entering
    the numbers on a new line.

    Attributes
    ----------
    input : str
        The special form input string to interpret.
    total_rows : int
        The total number of rows in the dataset.
    zero_indexed : bool
        Whether the rows are zero-indexed or not.
    _FORM_TO_OPERATION : dict[SelectionForm, Callable]
        A dictionary that maps the selection form to the operation to be
        performed on the selected rows.
    """

    def __init__(
        self,
        input: str,
        total_rows: int,
        *,
        zero_indexed: bool = False,
    ) -> None:
        self.input: str = input
        self.length: int = total_rows
        self._selected_rows: set[int] = set()
        self.zero_indexed: bool = zero_indexed

        self._FORM_TO_OPERATION: dict[SelectionForm, Callable] = {
            SelectionForm.SINGLE: self._add_single_row,
            SelectionForm.FROM: self._add_rows_from,
            SelectionForm.TO: self._add_rows_to,
            SelectionForm.RANGE: self._add_row_range,
        }

    def interpret(self) -> list[int]:
        """Interprets string input to a list of numbers that can be used to
        select indices from a DataFrame.

        Returns
        -------
        list[int]
            The sorted numbers to be used to select rows from a DataFrame.
        """
        for line in self.input.split():
            self._validate_and_interpret_line(line)

        return sorted(self._selected_rows)

    def _get_digit_and_form(
        self, line: str
    ) -> tuple[int, SelectionForm] | tuple[tuple[int, int], SelectionForm]:
        """Extracts the digit and the form of the line.

        Parameters
        ----------
        line : str
            the original input form of the line.

        Returns
        -------
        tuple[int, SelectionForm]
            The digit extracted from the form of the line.
        tuple[tuple[int, int], SelectionForm]
            The range of digits extracted from the form of the line.
        """
        if line.isdigit():
            digit = self._adjust_index(int(line))
            return (digit, SelectionForm.SINGLE)
        elif self._is_plus(line):
            digit = self._adjust_index(int(line[:-1]))
            return (digit, SelectionForm.FROM)
        elif self._is_minus(line):
            digit = self._adjust_index(int(line[1:]))
            return (digit, SelectionForm.TO)
        elif self._is_range(line):
            lower, upper = map(int, line.split("-"))
            lower = self._adjust_index(lower)
            upper = self._adjust_index(upper)
            if lower > upper:
                lower, upper = upper, lower
            return (lower, upper), SelectionForm.RANGE

        raise ValueError(f"Unknown form `{line}`")

    def _validate_and_interpret_line(self, line: str) -> None:
        """Validates the line form then interprets it to the digits to be added
        to the row selection set `_selected_rows`.

        Parameters
        ----------
        line : str
            the original input form of the line.

        Raises
        ------
        ValueError
            Arises when the line doesn't match any of the supported forms.
        """
        digit, form = self._get_digit_and_form(line)
        self._validate_digit_in_range(line, digit)
        self._FORM_TO_OPERATION[form](digit)

    def _validate_digit_in_range(
        self, line: str, digit: int | tuple[int, int]
    ) -> None:
        """A validator function to check whether the digits from a line
        is inside the range of dataset length (0-N) where N is Length

        Parameters
        ----------
        digit : int | tuple[int, int]
            the digit or range of digits extracted from the entered form
        line : str
            in the original form entered by the user

        Examples
        --------
            >>> 1
            >>> -2
            >>> 5+
            >>> 2-5

        Raises
        ------
        ValueError
            Shows on which digit & in which line responsible for out of range
            error
        """
        digits = [digit] if isinstance(digit, int) else list(digit)
        for digit in digits:
            if not self._in_range(digit):
                correct_range: str = (
                    f"(0-{self.length - 1})"
                    if self.zero_indexed
                    else f"(1-{self.length})"
                )
                if not self.zero_indexed:
                    digit += 1
                raise ValueError(
                    f"Digit {digit} of line `{line}` is out of your dataset "
                    f"range, please pick a number between {correct_range}"
                )

    def _is_minus(self, input: str) -> bool:
        """Checks whether the input form abides to _add_rows_to method

        Examples
        --------
        >>> -2
        >>> -5
        >>> -(N-1)
        Where N is equal to the length of the dataset

        Parameters
        ----------
        input : str
            the original input from user input line

        Returns
        -------
        bool
            True if it falls under the noted form
            False otherwise
        """
        return input.startswith("-") and self._is_integer(input[1:])

    def _is_plus(self, input: str) -> bool:
        """Checks whether the input form abides to _add_rows_to method

        Examples
        --------
        >>> 2+
        >>> 5+
        >>> Z+
        where 0 <= Z < N

        Parameters
        ----------
        input : str
            the original input from user input line

        Returns
        -------
        bool
            True if it falls under the noted form
            False otherwise
        """
        return input.endswith("+") and self._is_integer(input[:-1])

    def _is_range(self, input: str) -> bool:
        """Checks whether the input form abides to _add_row_range method

        Examples
        --------
        >>> 17-20

        Parameters
        ----------
        input : str
            the original input from user input line

        Returns
        -------
        bool
            True if it falls under the noted form
            False otherwise
        """
        if "-" not in input or input.count("-") > 1:
            return False

        l, r = input.split("-")
        return self._is_integer(l) and self._is_integer(r)

    def _in_range(self, *digits: int) -> bool:
        """Checks whether the digit is in range of the dataset

        Returns
        -------
        bool
            True if digit is greater than and equal 0
            and less than dataset length
            False otherwise
        """
        return all(0 <= digit < self.length for digit in digits)

    def _add_single_row(self, digit: int) -> None:
        """Adds a single row to the selected rows.

        Parameters
        ----------
        digit : int
            The row number to add.
        """
        self._selected_rows.add(digit)

    def _add_rows_to(self, digit: int) -> None:
        """Adds all rows from the first row to the specified row.

        Examples
        --------
        >>> -2 => {0, 1, 2}
        >>> -5 => {0, 1, 2, 3, 4, 5}

        Parameters
        ----------
        digit : int
            The last row number to add.
        """
        self._selected_rows.update(range(0, digit + 1))

    def _add_rows_from(self, digit: int) -> None:
        """Adds all rows from the specified row to the last row.

        Examples
        --------
        >>> 50+ => {50, 51, 52, ....., N-1}

        Parameters
        ----------
        digit : int
            The first row number to add.
        """
        self._selected_rows.update(range(digit, self.length))

    def _add_row_range(self, rng: tuple[int, int]) -> None:
        """Adds all rows in the specified range.

        Examples
        --------
        >>> 17-20 => {17, 18, 19, 20}

        Parameters
        ----------
        lower : int
            The first row number in the range.
        upper : int
            The last row number in the range.
        """
        lower, upper = rng
        self._selected_rows.update(range(lower, upper + 1))

    def _is_integer(self, input: str) -> bool:
        """Checks whether the input can be converted to an integer."""
        return input.isdigit()

    def _adjust_index(self, digit: int) -> int:
        """Adjusts the digit index to zero or one indexed."""
        return digit - (not self.zero_indexed)
