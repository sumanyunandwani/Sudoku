from copy import copy
from typing import List

class Sudoku(object):
    
    def __init__(self, grid: List[List[int]]) -> None:
        
        self.grid = grid
        self.__rows = len(grid)
        self.__cols = len(grid[0])
        self.__potential = [ [set( [ 1,2,3,4,5,6,7,8,9 ] ) for _ in range( self.__cols ) ] for _ in range( self.__rows ) ]
    
    
    def solve(self) -> List[List[int]]:
        
        return self.__main_solution()
    
    def __main_solution(self) -> List[List[int]]:
        
        return self.__position_knowns()
    
    def __is_safe(self, grid, i, j):
        
        for col in range(self.__cols):
            if col != j and grid[i][col] == grid[i][j]:
                return False 
            
        for row in range(self.__rows):
            if row != i and grid[row][j] == grid[i][j]:
                return False 
        
        box_i = (i // 3) * 3
        box_j = (j // 3) * 3

        for row in range(box_i, box_i + 3):
            for col in range(box_j, box_j + 3):
                if row == i and col == j:
                    continue
                elif grid[row][col] == grid[i][j]:
                    return False
        
        return True


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
                    

    def __position_knowns(self):
        
        self.__update_potatials()

        if not self.__find_constants():
            grid = copy(self.grid)
            self.grid = self.__guessing(grid)
        return True
    
    def __find_constants(self):

        found_something = True

        count = 0

        while found_something:

            print(count)
            count += 1
            found_something = False

            for i in range( self.__rows ):
                for j in range( self.__cols ):
                    if len( self.__potential[i][j] ) == 1:

                        found_something = True
                        
                        self.grid[i][j] = self.__potential[i][j].pop()
                
                        self.__update_potential_for_indexes(i, j)
                        
        return self.__is_complete()


    def __is_complete(self):
        
        for i in range( self.__rows ):
            for j in range( self.__cols ):
                if self.grid[i][j] == 0: 
                    return False
        return True
    

    def __update_potatials(self) -> None:
        
        for i in range( self.__rows ):
            for j in range( self.__cols ):
                if self.grid[i][j] != 0:
                    
                    self.__potential[i][j] = set()
                    self.__update_potential_for_indexes(i, j)
        
    def __update_potential_for_indexes(self, i: int, j: int) -> None:
        
        value = self.grid[i][j]
        
        for row_index in range( self.__rows ):
            self.__potential[row_index][j].discard(value)
        
        for col_index in range( self.__cols ):
            self.__potential[i][col_index].discard(value)

        box_no = 3 * ( i // 3 ) + ( j // 3 )

        self.__update_box(box_no, value)

    def __update_box(self, box_no: int, value: int) -> None:
        
        starting_row = (box_no // 3) * 3
        starting_col = ( box_no % 3 ) * 3

        for i in range(starting_row, starting_row + 3):
            for j in range(starting_col, starting_col + 3):
                self.__potential[i][j].discard(value)

    

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
        [0, 0, 4, 0, 9, 0, 7, 0, 6],
        [6, 8, 0, 0, 5, 0, 0, 2, 0],
        [0, 0, 0, 8, 0, 7, 4, 0, 0],
        [7, 0, 0, 0, 4, 1, 2, 0, 3],
        [3, 0, 0, 9, 0, 0, 0, 0, 4],
        [0, 6, 0, 0, 0, 2, 8, 0, 0],
        [0, 7, 6, 4, 2, 5, 9, 0, 0],
        [2, 4, 0, 3, 0, 9, 0, 7, 0],
        [8, 3, 0, 7, 0, 6, 0, 4, 2]
    ],
    [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],  
        [6, 8, 0, 0, 7, 0, 0, 9, 0],  
        [1, 9, 0, 0, 0, 4, 5, 0, 0],  
        [8, 2, 0, 1, 0, 0, 0, 4, 0],  
        [0, 0, 4, 6, 0, 2, 9, 0, 0],  
        [0, 5, 0, 0, 0, 3, 0, 2, 8],  
        [0, 0, 9, 3, 0, 0, 0, 7, 4],  
        [0, 4, 0, 0, 5, 0, 0, 3, 6],  
        [7, 0, 3, 0, 1, 8, 0, 0, 0]  
    ],
    [   
        [5, 3, 0, 0, 7, 0, 0, 0, 0],  
        [6, 0, 0, 1, 9, 5, 0, 0, 0],  
        [0, 9, 8, 0, 0, 0, 0, 6, 0],  
        [8, 0, 0, 0, 6, 0, 0, 0, 3],  
        [4, 0, 0, 8, 0, 3, 0, 0, 1],  
        [7, 0, 0, 0, 2, 0, 0, 0, 6],  
        [0, 6, 0, 0, 0, 0, 2, 8, 0],  
        [0, 0, 0, 4, 1, 9, 0, 0, 5],  
        [0, 0, 0, 0, 8, 0, 0, 7, 9]  
    ],
    [
        [1, 0, 0, 0, 0, 7, 0, 9, 0],  
        [0, 3, 0, 0, 2, 0, 0, 0, 8],  
        [0, 0, 9, 6, 0, 0, 5, 0, 0],  
        [0, 0, 5, 3, 0, 0, 9, 0, 0],  
        [0, 1, 0, 0, 8, 0, 0, 0, 2],  
        [6, 0, 0, 0, 0, 4, 0, 0, 0],  
        [3, 0, 0, 0, 0, 0, 0, 1, 0],  
        [0, 4, 0, 0, 0, 0, 0, 0, 7],  
        [0, 0, 7, 0, 0, 0, 3, 0, 0]  
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
    print("Puzzle #{}: {}".format(index+1, obj.solve()))