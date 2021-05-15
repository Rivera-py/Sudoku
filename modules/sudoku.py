"""
Module with an object holding a suite of attributes and methods to help with Sudoku solution.

Required:
  - Stated imports
  - Instantiated logger
"""


import json


class Sudoku()
    """Sudoku object class."""

    def __init__(self, encoded_sudoku, logger=""):
        """Constructor, initialising Sudoku object."""

        self.sudoku_rows = self.decode_json(encoded_sudoku)
        self.log = logger

    @staticmethod
    def decode_json(json_string):
        """Turns JSON string dump into python readable data."""

        return json.load(json_string)