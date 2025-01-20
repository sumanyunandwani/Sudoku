# ----------------- Importing Modules -----------------------
from copy import copy
from typing import List

# ----------------- Sudoku Class Initiation -----------------------
"""
Sudoku Class
Objective: Solve a 9X9 Sudoku
Input: 9X9 Grid, 2-D Array, Integer Datatype, with empty blocks displayed by 0
Output: 9X9 Grid, 2-D Array, Integer Datatype, all blocks filled 
"""
class Sudoku(object):
    

    """
    Constructor
    Objective: Initialize variables
    Input: 9X9 Grid, 2-D Array of Integer Datatypes
    Output: Nothing
    """
    def __init__(self, grid: List[List[int]]) -> None:
        
        self.grid = grid
        self.__rows = len(grid)
        self.__cols = len(grid[0])
        self.__note = [ [set( [ 1,2,3,4,5,6,7,8,9 ] ) for _ in range( self.__cols ) ] for _ in range( self.__rows ) ]
    
    
    """
    Solve Method
    Objective: Solve the 9X9 Grid
    Input: Nothing
    Output: 9X9 Grid, 2-D Array of Integer Datatypes
    """
    def solve(self) -> List[List[int]]:
        
        return self.__solve_9X9()
    

    """
    ProSolve 9X9 Method: Private Method
    Objective: Solve the 9X9 Grid
    Input: Nothing
    Output: 9X9 Grid, 2-D Array of Integer Datatypes
    """
    def __solve_9X9(self) -> List[List[int]]:
        
        self.__sumanyu_algorithm()

        if not self.__is_complete():

            self.grid = self.__guessing(copy(self.grid))
        
        return self.grid if self.grid else "Kindly check the validity of the Puzzle"

    """
    Sumanyu Algorithm
    Objective: Executed Algorithm created by Sumanyu
    Input: Nothing
    Output: Nothing
    """
    def __sumanyu_algorithm(self):

        self.__make_notes()

        found_something = True

        while found_something:

            found_something = False

            for i in range( self.__rows ):

                for j in range( self.__cols ):

                    if len( self.__note[i][j] ) == 1:

                        found_something = True
                        
                        self.grid[i][j] = self.__note[i][j].pop()
                
                        self.__update_notes_for_indexes(i, j)

    """
    Make Notes
    Objective: Generate initial notes values for each cell
    Input: Nothing
    Output: Nothing
    """
    def __make_notes(self) -> None:
        
        for i in range( self.__rows ):
            
            for j in range( self.__cols ):
                
                if self.grid[i][j] != 0:
                    
                    self.__note[i][j] = set()
                    
                    self.__update_notes_for_indexes(i, j)

    """
    Is Safe
    Objective: Check if placing a value at position (i, j) in the grid is valid.
    Input:
        - grid: 2D List representing the Sudoku grid.
        - i: Row index of the cell.
        - j: Column index of the cell.
    Output: Boolean value indicating whether the value at (i, j) is valid.
    """
    def __is_safe(self, grid, i, j):
        
        return self.__is_safe_row(grid, i, j) and self.__is_safe_col(grid, i, j) and self.__is_sage_box(grid, i, j)
    
    """
    Is Sage Row
    Objective: Check if the value at grid[i][j] is unique in its row.
    Input:
        - grid: 2D List representing the Sudoku grid.
        - i: Row index of the cell.
        - j: Column index of the cell.
    Output: Boolean value indicating if the row is valid for the value at (i, j).
    """
    def __is_safe_row(self, grid: List[List[int]], i: int, j: int) -> bool:
        
        return not any(grid[row][j] == grid[i][j] and row != i for row in range(self.__rows))

    """
    Is Safe Col
    Objective: Check if the value at grid[i][j] is unique in its column.
    Input:
        - grid: 2D List representing the Sudoku grid.
        - i: Row index of the cell.
        - j: Column index of the cell.
    Output: Boolean value indicating if the column is valid for the value at (i, j).
    """
    def __is_safe_col(self, grid: List[List[int]], i: int, j: int) -> bool:
        
        return not any(grid[i][col] == grid[i][j] and col != j for col in range(self.__cols))

    """
    Is Safe Box
    Objective: Check if the value at grid[i][j] is unique in its 3x3 subgrid.
    Input:
        - grid: 2D List representing the Sudoku grid.
        - i: Row index of the cell.
        - j: Column index of the cell.
    Output: Boolean value indicating if the 3x3 subgrid is valid for the value at (i, j).
    """
    def __is_sage_box(self, grid: List[List[int]], i: int, j: int) -> bool:
        
        for row in range((i // 3) * 3, (i // 3) * 3 + 3):
            
            for col in range((j // 3) * 3, (j // 3) * 3 + 3):
                
                if grid[row][col] == grid[i][j] and row != i and col != j:
                    
                    return False
        
        return True

    """
    Guessing
    Objective: Attempt to solve the grid using backtracking if other methods fail
    Input: Current grid
    Output: Solved grid or False if no solution exists
    """
    def __guessing(self, grid):
        
        for i in range(self.__rows):
            
            for j in range(self.__cols):
                
                if grid[i][j] == 0:
                    
                    for num in range(1, 10):
                        
                        grid[i][j] = num
                        
                        if self.__is_safe(grid, i, j) and self.__guessing(grid):
                            
                            return grid

                        grid[i][j] = 0
                    
                    if grid[i][j] == 0: return False

        return True
    
    """
    Is Complete
    Objective: Check if the grid is fully solved
    Input: Nothing
    Output: Boolean - True if complete, False otherwise
    """
    def __is_complete(self) -> bool:
        
        return all(self.grid[i][j] != 0 for i in range(self.__rows) for j in range(self.__cols))
    
    """
    Update Notes for Indexes
    Objective: Update notes values for cells in the same row, column, and box as a given cell
    Input: Row index, column index
    Output: Nothing
    """
    def __update_notes_for_indexes(self, i: int, j: int) -> None:
        
        value = self.grid[i][j]
        
        for row_index in range( self.__rows ):
            
            self.__note[row_index][j].discard(value)
        
        for col_index in range( self.__cols ):
            
            self.__note[i][col_index].discard(value)

        self.__update_box(3 * ( i // 3 ) + ( j // 3 ), value)

    """
    Update Box
    Objective: Update Notes values for cells in a specific 3x3 box
    Input: Box number, value to remove
    Output: Nothing
    """
    def __update_box(self, box_no: int, value: int) -> None:
        
        for i in range((box_no // 3) * 3, (box_no // 3) * 3 + 3):           
            
            for j in range(( box_no % 3 ) * 3, ( box_no % 3 ) * 3 + 3):     
                
                self.__note[i][j].discard(value)

    
# ----------------- Main Code for this file -----------------------
if __name__ == "__main__":

    grids = [
        [
            [ 0, 0, 0, 2, 6, 0, 7, 0, 1 ],
            [ 6, 8, 0, 0, 7, 0, 0, 9, 0 ],
            [ 1, 9, 0, 0, 0, 4, 5, 0, 0 ],
            [ 8, 2, 0, 1, 0, 0, 0, 4, 0 ],
            [ 0, 0, 4, 6, 0, 2, 9, 0, 0 ],
            [ 0, 5, 0, 0, 0, 3, 0, 2, 8 ],
            [ 0, 0, 9, 3, 0, 0, 0, 7, 4 ],
            [ 0, 4, 0, 0, 5, 0, 0, 3, 6 ],
            [ 7, 0, 3, 0, 1, 8, 0, 0, 0 ]
        ],
        [
            [5, 0, 1, 6, 9, 0, 0, 7, 2],
            [9, 8, 0, 3, 0, 2, 1, 0, 4],
            [7, 0, 0, 0, 0, 0, 6, 9, 0],
            [0, 0, 0, 7, 0, 1, 5, 0, 0],
            [0, 6, 0, 9, 0, 0, 7, 0, 1],
            [4, 1, 0, 5, 0, 0, 0, 0, 3],
            [3, 0, 0, 0, 0, 7, 4, 6, 0],
            [0, 5, 0, 8, 0, 0, 0, 0, 0],
            [0, 7, 2, 0, 6, 0, 0, 0, 9]
        ],
        [
            [0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 3],
            [0, 7, 4, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 2],
            [0, 8, 0, 0, 4, 0, 0, 1, 0],
            [6, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 7, 8, 0],
            [5, 0, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0]
        ]
    ]

    for index, grid in enumerate(grids):
        
        obj = Sudoku(grid)
        
        print("Puzzle #{number}: {problem}\n".format(number=index+1, problem=grid))
        print("Solution #{number}: {solution}\n".format(number=index+1, solution=obj.solve()))
