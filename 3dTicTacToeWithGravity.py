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

def formattedGrid(grid):
    return [[[cell[0] for cell in row] for row in floor] for floor in grid]

def win(winner):
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

def checkfor3s(grid):
    global winner
    for floor in grid:
        floorFormatted = [[cell[0] for cell in row] for row in floor]
        won = checkFloor(floorFormatted)
        if won != None:
            winner = won
            return winner
    wholeFormatted = formattedGrid(grid)
    wholeFormattedFlipped = flip(wholeFormatted)
    for floor in wholeFormattedFlipped:
        won = checkFloor(floor)
        if won != None:
            winner = won
            return winner
    won = check3dDiagonals(wholeFormattedFlipped)
    if won != None:
        winner = won
        return winner
    return False

def check(x, y, floor):
    check1 = False
    check2 = False
    print("FLOOR:", floor, "ROW:", y, "COL:", x)
    if floor > 0:
        if floor > 1:
            if grid[floor-2][y][x][0] != "":
                check2 = True
        if grid[floor-1][y][x][0] != "":
            check1 = True
    if not (((floor > 1 and check1) and check2) or (floor == 1 and check1) or (floor == 0)):
        return False
    return True

def modifyBoard(x, y, floor, rep):
    print(floor)
    space = grid[floor][y][x]
    space[0] = rep
    butt = space[1]
    butt.config(text=rep)
    butt.state(["disabled"])

def change(x, y, floor, root):
    global activePlayer
    if check(x, y, floor):
        modifyBoard(x, y, floor, activePlayer)
    match activePlayer:
        case "X":
            activePlayer = "O"
        case "O":
            activePlayer = "X"
    root.title(f"3D Tic Tac Toe with gravity - {activePlayer}'s turn")
    winner = checkfor3s(grid)
    if winner:
        win(winner)

def ai(grid):
    f, r, c = 0, 0, 0
    possibleMoves = [[[False, False, False] for _ in range(3)] for _ in range(3)]
    for floor in grid:
        for row in floor:
            for col in row:
                if check(c, r, f) and formattedGrid(grid)[f][r][c] != "O":
                    print(possibleMoves)
                    possibleMoves[f][r][c] = True
                c += 1
            c = 0
            r += 1
        r = 0
        f += 1
    f = 0
    winningMoves = []
    for floor in possibleMoves:
        for row in floor:
            for col in row:
                if col:
                    potgrid = [x for x in grid]
                    potgrid[f][r][c][0] = "X"
                    if checkfor3s(potgrid) == "X":
                        winningMoves.append([f, r, c])
                c += 1
            c = 0
            r += 1
        r = 0
        f += 1
    f = 0
    if len(winningMoves) == 0:
        global movex, movey, movef 
        movex, movey, movef = 0,0,0
        for floor in grid:
            for row in floor:
                for col in row:
                    if check(c, r, f) and formattedGrid(grid)[f][r][c] != "O":
                        movex = c
                        movey = r
                        movef = f
                        break
                    c += 1
                c = 0
                r += 1
            r = 0
            f += 1
        c = 0
        r = 0
        f = 0
        modifyBoard(movex, movey, movef, "X")
    else:
        print(winningMoves)


def changeAI(x, y, floor):
    modifyBoard(x, y, floor, "O")
    print(checkfor3s(grid))
    ai(grid)
    print(checkfor3s(grid))

def human():
    global rootroot
    rootroot.withdraw()
    root = tk.Toplevel(rootroot)
    root.title("3D Tic Tac Toe with gravity - X's turn")
    root.geometry("1350x300")
    root.columnconfigure(list(range(12)), weight=1, uniform="Silent_Creme")
    root.rowconfigure(list(range(12)), weight=1, uniform="Silent_Creme")
    for f in range(3):
        floor = ttk.Frame(root)
        floor.grid(column=f*4,row=0,columnspan=3,rowspan=3)
        for i in range(3):
            for j in range(3):
                butt = ttk.Button(floor, text="", command=partial(change, i, j, f, root))
                butt.grid(row=j, column=i, ipadx=25, ipady=30)
                grid[f][j][i].append(butt)

    root.mainloop()

def computer():
    global rootroot
    rootroot.withdraw()
    root = tk.Toplevel(rootroot)
    root.title("3D Tic Tac Toe with gravity - vs AI")
    root.geometry("1350x300")
    root.columnconfigure(list(range(12)), weight=1, uniform="Silent_Creme")
    root.rowconfigure(list(range(12)), weight=1, uniform="Silent_Creme")
    for f in range(3):
        floor = ttk.Frame(root)
        floor.grid(column=f*4,row=0,columnspan=3,rowspan=3)
        for i in range(3):
            for j in range(3):
                butt = ttk.Button(floor, text="", command=partial(changeAI, i, j, f))
                butt.grid(row=j, column=i, ipadx=25, ipady=30)
                grid[f][j][i].append(butt)
    ai(grid)
    root.mainloop()

def main():
    global rootroot
    rootroot = tk.Tk()
    rootroot.geometry("240x50")
    rootroot.title("3D Tic Tac Toe with gravity - Choose computer or human")
    label = ttk.Label(rootroot, text="Choose computer or human").grid(row=0,column=0)
    button = ttk.Button(rootroot, text="Computer", command=computer).grid(row=1, column=0)
    button2 = ttk.Button(rootroot, text="Human", command=human).grid(row=1, column=2)
    quitk = tk.Tk()
    quitbtn = ttk.Button(quitk, text="quit", command=exit).pack()
    rootroot.mainloop()
    quitk.mainloop
    

if __name__ == "__main__":
    main()
