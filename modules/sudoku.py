"""Module with an object holding a suite of attributes and methods to help with Sudoku solution."""

class Sudoku()
    """Sudoku object class."""

    def __init__(self, encoded_sudoku, logger=""):
        """Constructor, initialising Sudoku object."""

        self.sudoku = self.decode_json(encoded_sudoku)
        self.log = logger
