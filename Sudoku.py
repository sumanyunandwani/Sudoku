"""Module providing a class to solve Sudoku 9X9 puzzles"""

from copy import copy
from typing import List


class Sudoku:
    """
    Sudoku Class
    Objective: Solve a 9X9 Sudoku
    Input: 9X9 Grid, 2-D Array, Integer Datatype, with empty blocks displayed by 0
    Output: 9X9 Grid, 2-D Array, Integer Datatype, all blocks filled 
    """

    def __init__(self, grid: List[List[int]]) -> None:
        """
        Objective: Initialize variables
        Input: 9X9 Grid, 2-D Array of Integer Datatypes
        Output: Nothing
        """

        self.grid = grid
        self.__rows = len(grid)
        self.__cols = len(grid[0])
        self.__note = [
            [
                set( [ 1,2,3,4,5,6,7,8,9 ] )
                for _ in range( self.__cols )
            ]
            for _ in range( self.__rows )
        ]


    def solve(self) -> List[List[int]]:
        """
        Objective: Solve the 9X9 Grid
        Input: Nothing
        Output: 9X9 Grid, 2-D Array of Integer Datatypes
        """

        return self.__solve9X9()

    def __solve9X9(self) -> List[List[int]]:
        """
        ProSolve 9X9 Method: Private Method
        Objective: Solve the 9X9 Grid
        Input: Nothing
        Output: 9X9 Grid, 2-D Array of Integer Datatypes
        """

        self.__sumanyuAlgorithm()

        if not self.__isComplete():

            self.grid = self.__guessing(copy(self.grid))

        return self.grid if self.grid else "Kindly check the validity of the Puzzle"

    def __sumanyuAlgorithm(self):
        """
        Sumanyu Algorithm
        Objective: Executed Algorithm created by Sumanyu
        Input: Nothing
        Output: Nothing
        """

        self.__makeNotes()

        found_something = True

        while found_something:

            found_something = False

            for i in range( self.__rows ):

                for j in range( self.__cols ):

                    if len( self.__note[i][j] ) == 1:

                        found_something = True

                        self.grid[i][j] = self.__note[i][j].pop()

                        self.__updateNotesForIndexes(i, j)


    def __makeNotes(self) -> None:
        """
        Make Notes
        Objective: Generate initial notes values for each cell
        Input: Nothing
        Output: Nothing
        """

        for i in range( self.__rows ):

            for j in range( self.__cols ):

                if self.grid[i][j] != 0:

                    self.__note[i][j] = set()

                    self.__updateNotesForIndexes(i, j)


    def __isSafe(self, grid: List[List[int]], i: int, j: int) -> bool:
        """
        Is Safe
        Objective: Check if placing a value at position (i, j) in the grid is valid.
        Input:
            - grid: 2D List representing the Sudoku grid.
            - i: Row index of the cell.
            - j: Column index of the cell.
        Output: Boolean value indicating whether the value at (i, j) is valid.
        """
        return (
            self.__isSafeRow(grid, i, j) and
            self.__isSafeCol(grid, i, j) and
            self.__isSafeBox(grid, i, j)
        )

    def __isSafeRow(self, grid: List[List[int]], i: int, j: int) -> bool:
        """
        Is Sage Row
        Objective: Check if the value at grid[i][j] is unique in its row.
        Input:
            - grid: 2D List representing the Sudoku grid.
            - i: Row index of the cell.
            - j: Column index of the cell.
        Output: Boolean value indicating if the row is valid for the value at (i, j).
        """
        return not any(grid[row][j] == grid[i][j] and row != i for row in range(self.__rows))


    def __isSafeCol(self, grid: List[List[int]], i: int, j: int) -> bool:
        """
        Is Safe Col
        Objective: Check if the value at grid[i][j] is unique in its column.
        Input:
            - grid: 2D List representing the Sudoku grid.
            - i: Row index of the cell.
            - j: Column index of the cell.
        Output: Boolean value indicating if the column is valid for the value at (i, j).
        """
        return not any(grid[i][col] == grid[i][j] and col != j for col in range(self.__cols))


    def __isSafeBox(self, grid: List[List[int]], i: int, j: int) -> bool:
        """
        Is Safe Box
        Objective: Check if the value at grid[i][j] is unique in its 3x3 subgrid.
        Input:
            - grid: 2D List representing the Sudoku grid.
            - i: Row index of the cell.
            - j: Column index of the cell.
        Output: Boolean value indicating if the 3x3 subgrid is valid for the value at (i, j).
        """
        for row in range((i // 3) * 3, (i // 3) * 3 + 3):

            for col in range((j // 3) * 3, (j // 3) * 3 + 3):

                if grid[row][col] == grid[i][j] and row != i and col != j:

                    return False

        return True


    def __guessing(self, grid: List[List[int]]) -> List[List[int]]:
        """
        Guessing
        Objective: Attempt to solve the grid using backtracking if other methods fail
        Input: Current grid
        Output: Solved grid or False if no solution exists
        """
        for i in range(self.__rows):

            for j in range(self.__cols):

                if grid[i][j] == 0:

                    for num in range(1, 10):

                        grid[i][j] = num

                        if self.__isSafe(grid, i, j) and self.__guessing(grid):

                            return grid

                        grid[i][j] = 0

                    if grid[i][j] == 0:
                        return False

        return True


    def __isComplete(self) -> bool:
        """
        Is Complete
        Objective: Check if the grid is fully solved
        Input: Nothing
        Output: Boolean - True if complete, False otherwise
        """
        return all(self.grid[i][j] != 0 for i in range(self.__rows) for j in range(self.__cols))


    def __updateNotesForIndexes(self, i: int, j: int) -> None:
        """
        Update Notes for Indexes
        Objective: Update notes values for cells in the same row, column, and box as a given cell
        Input: Row index, column index
        Output: Nothing
        """
        value = self.grid[i][j]

        for row_index in range( self.__rows ):

            self.__note[row_index][j].discard(value)

        for col_index in range( self.__cols ):

            self.__note[i][col_index].discard(value)

        self.__updateBox(3 * ( i // 3 ) + ( j // 3 ), value)


    def __updateBox(self, box_no: int, value: int) -> None:
        """
        Update Box
        Objective: Update Notes values for cells in a specific 3x3 box
        Input: Box number, value to remove
        Output: Nothing
        """
        for i in range((box_no // 3) * 3, (box_no // 3) * 3 + 3):

            for j in range(( box_no % 3 ) * 3, ( box_no % 3 ) * 3 + 3):

                self.__note[i][j].discard(value)
# End-of-file (EOF)
