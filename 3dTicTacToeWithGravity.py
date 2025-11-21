import tkinter as tk
from tkinter import ttk
from functools import partial
import time

grid = [[[[""], [""], [""]] for _ in range(3)] for _ in range(3)]
activePlayer = "X"
winner = None

def check3dDiagonals(grid):
    if grid[0][0][0] != "" and grid[0][0][0] == grid[1][1][1] == grid[2][2][2]:
        return grid[0][0][0]
    if grid[0][0][2] != "" and grid[0][0][2] == grid[1][1][1] == grid[2][2][0]:
        return grid[0][0][2]
    if grid[0][0][1] != "" and grid[0][0][1] == grid[1][1][1] == grid[2][2][1]:
        return grid[0][0][1]
    return None

def flip(grid):
    return [list(col) for col in zip(*grid)]

def win():
    print(f"{winner} won")
    time.sleep(5)
    exit()

def checkFloor(floor):
    for row in floor:
        if row[0] != "" and row[0] == row[1] == row[2]:
            return row[0]

    for col in range(3):
        if floor[0][col] != "" and floor[0][col] == floor[1][col] == floor[2][col]:
            return floor[0][col]

    if floor[0][0] != "" and floor[0][0] == floor[1][1] == floor[2][2]:
        return floor[0][0]

    if floor[0][2] != "" and floor[0][2] == floor[1][1] == floor[2][0]:
        return floor[0][2]

    return None

def check():
    global winner
    for floor in grid:
        floorFormatted = [[cell[0] for cell in row] for row in floor]
        won = checkFloor(floorFormatted)
        if won != None:
            winner = won
            win()
    wholeFormatted = [[[cell[0] for cell in row] for row in floor] for floor in grid]
    wholeFormattedFlipped = flip(wholeFormatted)
    for floor in wholeFormattedFlipped:
        won = checkFloor(floor)
        if won != None:
            winner = won
            win()
    won = check3dDiagonals(wholeFormattedFlipped)
    if won != None:
        winner = won
        win()
    print(wholeFormattedFlipped)

def change(x, y, floor):
    global activePlayer
    check1 = False
    check2 = False
    if floor > 0:
        if floor > 1:
            if grid[floor-2][y][x][0] != "":
                check2 = True
        if grid[floor-1][y][x][0] != "":
            check1 = True
    if not (((floor > 1 and check1) and check2) or (floor == 1 and check1) or (floor == 0)):
        return
    space = grid[floor][y][x]
    space[0] = activePlayer
    butt = space[1]
    butt.config(text=activePlayer)
    butt.state(["disabled"])
    match activePlayer:
        case "X":
            activePlayer = "O"
        case "O":
            activePlayer = "X"
    root.title(f"3D Tic Tac Toe with gravity - {activePlayer}'s turn")
    check()
    


def main():
    global root
    root = tk.Tk()
    root.title("3D Tic Tac Toe with gravity - X's turn")
    root.geometry("1350x300")
    root.columnconfigure(list(range(12)), weight=1, uniform="Silent_Creme")
    root.rowconfigure(list(range(12)), weight=1, uniform="Silent_Creme")
    for f in range(3):
        floor = ttk.Frame(root)
        floor.grid(column=f*4,row=0,columnspan=3,rowspan=3)
        for i in range(3):
            for j in range(3):
                butt = ttk.Button(floor, text="", command=partial(change, i, j, f))
                butt.grid(row=j, column=i, ipadx=25, ipady=30)
                grid[f][j][i].append(butt)

    root.mainloop()

if __name__ == "__main__":
    main()
