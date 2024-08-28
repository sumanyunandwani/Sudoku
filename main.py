# ----------------- Importing Modules ----------------------------
import time
import numpy as np
from collections import defaultdict
# import logging

# logger = logging.getLogger(__name__)
# logging.basicConfig(filename="sudoku.log", filemode='w', level=logging.INFO)


# ----------------- Objects --------------------------------------
class Possibility(object):
    def __init__(self) -> None:
        self.s = 9
        self.array = [0 for i in range(self.s)]
        self.special = False
    
    def insert(self, number):
        self.array[number-1] = 1
    
    def remove(self, number):
        self.array[number-1] = 0
    
    def status(self):
        return self.array
    
    def getCount(self):
        return self.array.count(1)
    
    def getIndex(self):
        return self.array.index(1)
    

class Sudoku(object):
    def __init__(self, puzzle) -> None:
        self.puzzle = puzzle
        self.logicArray = np.array([])
        self.s = 9
        self.box = defaultdict(set)
        self.row = defaultdict(set)
        self.col = defaultdict(set)

    def executeLogic(self, count):
        start_time = time.time()
        print("Solving Sudoku #{}".format(count))
        answer = self.solveSudoku()
        end_time = time.time()
        print("Solved Sudoku #{} in {} seconds".format(count, end_time - start_time))
        return np.reshape(answer, (-1, 9))

    def solveSudoku(self):
        self.insertValue()
        for i in range(self.s):
            for j in range(self.s):
                if self.puzzle[i][j] != 0:
                    self.logicArray = np.append(self.logicArray, 0)
                else:
                    self.logicArray = np.append(self.logicArray, self.checkValue(i, j))
        self.logicArray = np.reshape(self.logicArray, (-1, 9))
            
        return self.solve()

    def insertValue(self):
        for i in range(self.s):
            for j in range(self.s):
                val = self.puzzle[i][j]
                if val != 0:
                    self.row[i].add(val)
                    self.col[j].add(val)
                    boxIndex = i//3*3 + j//3
                    self.box[boxIndex].add(val) 

    def checkValue(self, i, j):
        possibility = Possibility()
        for number in range(1, self.s+1):
            if self.isValid(number, i, j):
                possibility.insert(number)   
        print(possibility.status())     
        print(i,j)
        print(self.col[j])
        print(self.row[i])
        return possibility

    def isValid(self, number, i, j):
        if number in self.row[i] or number in self.col[j] or number in self.box[i//3*3 + j//3]:
            return False
        return True

    def solve(self):
        count = 0
        while (not np.array_equal(self.logicArray, np.array([[0 for _ in range(self.s)] for _ in range(self.s)])) and count<=5):
            for i in range(0, self.s, 3):
                for j in range(0, self.s, 3):
                    self.execute(i, j)
                    # if self.logicArray[i][j] != 0:
                    #     print(("{}\n".format(self.logicArray[i][j].status())))
            # if np.array_equal(logicArray, prevlogicArray):
            #     isSame = True
            #     print("Not able to solve this one!")
            count += 1
        # print(self.puzzle)
    # for m in range(self.s):
    #     for n in range(self.s):
    #         if self.logicArray[m][n] != 0:
    #             print(self.logicArray[m][n].status())
    # print(self.logicArray)
        print(self.puzzle)
        return self.puzzle

    def addList(self, list1, list2):
        return [item+list2[i] for i, item in enumerate(list1)]
        

    def execute(self, i, j):
        boxFreq = [0 for _ in range(self.s)]
        for row in range(i, i+3):
            for col in range(j, j+3):
                if self.logicArray[row][col] != 0 and self.logicArray[row][col].getCount() == 1:
                    index = self.logicArray[row][col].getIndex()
                    self.puzzle[row][col] = index + 1
                    self.logicArray[row][col] = 0
                    self.cleanup(index + 1, row, col)
        for row in range(i, i+3):
            for col in range(j, j+3):
                if self.logicArray[row][col] != 0:
                    boxFreq = self.addList(boxFreq, self.logicArray[row][col].status())
        print("Next")
        indexes = [index for index in range(len(boxFreq)) if boxFreq[index] == 1]
        if indexes:
            for row in range(i, i+3):
                for col in range(j, j+3):
                    if self.logicArray[row][col] != 0:
                        prob = self.logicArray[row][col].status()
                        print(prob)
                        print(row,col)
                        for index in indexes:
                            if prob[index] == 1:
                                self.puzzle[row][col] = index + 1
                                self.logicArray[row][col] = 0
                                self.cleanup(index + 1, row, col)


    def cleanup(self, number, row, col):
        for i in range(self.s):
            if self.logicArray[i][col] != 0:
                self.logicArray[i][col].remove(number)
            
            if self.logicArray[row][i] != 0:
                self.logicArray[row][i].remove(number)
        i = row//3
        j = col//3
        for m in range(i, i+3):
            for n in range(j, j+3):
                if self.logicArray[m][n] != 0:
                    self.logicArray[m][n].remove(number)
    
        






