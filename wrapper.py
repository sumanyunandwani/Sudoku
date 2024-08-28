# --------------------- Importing Modules -------------------------------
import pandas as pd
import numpy as np
open("sudoku.log", "w")
from main import Sudoku

# --------------------- Variables ---------------------------------------
filename = "C:/Users/suman/OneDrive/Documents/Github/sudoku.csv"
pd.options.display.max_rows = 99

# --------------------- Functions ---------------------------------------
def convertNumberToMatrix(x):
    array = np.array(list(map(float, str(x))))
    return np.reshape(array, (-1, 9))


# ---------------------- Main ------------------------------------------
if __name__ == "__main__":
    df = pd.read_csv(filename)
    print(df)
    """
    0120210201020120120210021 - 81 len
    [[9], [9], [9]..9]
    """
    df["quizzes"] = df["quizzes"].apply(convertNumberToMatrix)
    answer_array = []
    count = 0
    for puzzle in df['quizzes']:
        print(puzzle)
        obj = Sudoku(puzzle)
        answer_array.append(np.array(obj.executeLogic(count)))
        count += 1
        # if count == 0:
        #     answer_array = np.array(executeLogic(puzzle))
        # else:
        #     answer_array = np.append(answer_array, executeLogic(puzzle), axis=0)
        # print(answer_array)
        if count == 1:
            break 
        # count += 1
    s_df = pd.DataFrame(data={'solution': answer_array})
    

    df["solutions"] = df["solutions"].apply(convertNumberToMatrix) 

    if df["solutions"].equals(s_df):   
        print("Solved")
    else:
        print("False")
