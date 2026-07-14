import tkinter as tk
from tkinter import ttk, font
from functools import partial
import time

# TODO: implement AI

grid: list[list[list[list[ttk.Button | None]]]] = [
    [[[None], [None], [None]] for i in range(3)] for j in range(3)
]
activePlayer = "X"
winner = None


def check3dDiagonals(grid):
    if (
        grid[0][0][0] is not None
        and grid[0][0][0]
        == grid[1][1][1]
        == grid[2][2][2]
    ):
        return grid[0][0][0]

    if (
        grid[0][0][2] is not None
        and grid[0][0][2]
        == grid[1][1][1]
        == grid[2][2][0]
    ):
        return grid[0][0][2]

    if (
        grid[0][2][2] is not None
        and grid[0][2][2]
        == grid[1][1][1]
        == grid[2][0][0]
    ):
        return grid[0][2][2]

    if (
        grid[0][2][0] is not None
        and grid[0][2][0]
        == grid[1][1][1]
        == grid[2][0][2]
    ):
        return grid[0][2][0]

    return None


def flip(grid):
    return [list(col) for col in zip(*grid)]


def formattedGrid(grid):
    return [
        [
            [cell[0] for cell in row]
            for row in floor]
        for floor in grid
    ]


def win(winner):
    global grid
    print(f"{winner} won.")
    grid = [
        [[[None], [None], [None]] for i in range(3)] for j in range(3)
    ]
    time.sleep(3)
    human()


def checkFloor(floor):
    for row in floor:
        if (
            row[0] != ""
            and row[0]
            == row[1]
            == row[2]
        ):
            return row[0]

    for col in range(3):
        if (
            floor[0][col] != ""
            and floor[0][col]
            == floor[1][col]
            == floor[2][col]
        ):
            return floor[0][col]

    if (
        floor[0][0] != ""
        and floor[0][0]
        == floor[1][1]
        == floor[2][2]
    ):
        return floor[0][0]

    if (
        floor[0][2] != ""
        and floor[0][2]
        == floor[1][1]
        == floor[2][0]
    ):
        return floor[0][2]

    return None


def checkfor3s(grid):
    global winner
    for floor in grid:
        floorFormatted = [[cell[0] for cell in row] for row in floor]
        won = checkFloor(floorFormatted)
        if won is not None:
            winner = won
            return winner
    wholeFormatted = formattedGrid(grid)
    wholeFormattedFlipped = flip(wholeFormatted)
    for floor in wholeFormattedFlipped:
        won = checkFloor(floor)
        if won is not None:
            winner = won
            return winner
    for y in range(3):
        if (
            wholeFormatted[0][y][0] is not None
            and wholeFormatted[0][y][0]
            == wholeFormatted[1][y][1]
            == wholeFormatted[2][y][2]
        ):
            return wholeFormatted[0][y][0]

        if (
            wholeFormatted[0][y][2] is not None
            and wholeFormatted[0][y][2]
            == wholeFormatted[1][y][1]
            == wholeFormatted[2][y][0]
        ):
            return wholeFormatted[0][y][2]
    for x in range(3):
        if (
            wholeFormatted[0][0][x] is not None
            and wholeFormatted[0][0][x]
            == wholeFormatted[1][1][x]
            == wholeFormatted[2][2][x]
        ):
            return wholeFormatted[0][0][x]

        if (
            wholeFormatted[0][2][x] is not None
            and wholeFormatted[0][2][x]
            == wholeFormatted[1][1][x]
            == wholeFormatted[2][0][x]
        ):
            return wholeFormatted[0][2][x]
    won = check3dDiagonals(wholeFormattedFlipped)
    if won is not None:
        winner = won
        return winner
    return False


def check(x, y, floor):
    if grid[floor][y][x][0] is not None:
        return False

    if floor == 0:
        return True
    return grid[floor - 1][y][x][0] is not None


def modifyBoard(x, y, floor, rep):
    space = grid[floor][y][x]
    space[0] = rep
    butt = space[1]
    butt.config(text=rep)
    butt.state(["disabled"])


def change(x, y, floor, root):
    global activePlayer
    modded = False
    if check(x, y, floor):
        modifyBoard(x, y, floor, activePlayer)
        modded = True
    if modded:
        match activePlayer:
            case "X":
                activePlayer = "O"
            case "O":
                activePlayer = "X"
    root.title(f"3D Tic Tac Toe with gravity - {activePlayer}'s turn")
    winner = checkfor3s(grid)
    if winner:
        win(winner)


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
        floor.grid(column=f*4, row=0, columnspan=3, rowspan=4)
        for i in range(3):
            for j in range(3):
                butt = ttk.Button(
                    floor, text="", command=partial(change, i, j, f, root))
                butt.grid(row=j, column=i, ipadx=25, ipady=30)
                grid[f][j][i].append(butt)
        flrlbl = ttk.Label(floor, text=f"Floor {f}")
        flrlbl.grid(row=3, column=1, ipadx=25)

    root.mainloop()


def main():
    global rootroot
    rootroot = tk.Tk()
    TkHeadingFont = font.Font(size=29, family="Papyrus")
    papyrus = font.Font(size=13, family="Papyrus")
    rootroot.title("3D Tic Tac Toe with gravity")
    rootroot.config(bg="#1a1a1a")
    title = tk.Label(rootroot, text="3D Tic Tac Toe with gravity",
                     font=TkHeadingFont, bg="#1a1a1a", fg="white")
    title.grid(row=0, column=0)
    rules = tk.Label(rootroot, text="Regular tic tac toe rules apply, however you can also place ontop of other Xs or Os, and form diagonals/straight lines with those aswell.",
                     font=papyrus, bg="#1a1a1a", fg="white")
    rules.grid(row=1, column=0)
    button2 = ttk.Button(rootroot, text="Start",
                         command=human, padding=(20, 20))
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", background="#1a1a1a",
                    foreground="#2a2a2a", relief="raised")
    style.map("Tbutton",
              background=[("active", "#1a1a1a")],
              foreground=[("active", "#3a3a3a")])
    button2.grid(row=2, column=0)
    quitk = tk.Tk()
    quitbtn = ttk.Button(quitk, text="quit", command=exit)
    quitbtn.pack()
    rootroot.mainloop()
    quitk.mainloop


if __name__ == "__main__":
    main()
