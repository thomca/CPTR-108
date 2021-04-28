
ROWS = 20     # max Rows
COLS = 20     # max Cols
num_col = 20  # set Cols
num_row = 20  # set Rows
# initialize board with max size 
import display
board = display.Board(ROWS, COLS)


menuChoice = "0"
saveState = False
print("Welcome to Mine Sweeper!\nHere is your starting board.\n")
startChoice = input("Would you like to load(l) a save, or use a new game(other)?")
if startChoice == "l":
    saveState = board.loadState()
    
if saveState == False:
    while True:
        try:
            num_row = int(input("Number of Rows: "))
            num_col = int(input("Number of Columns: "))
            if num_row < 2 or num_row > ROWS or num_col < 2 or num_col > COLS:
                print("Try again")
                continue
        except(TypeError, ValueError):
            print("Invalid entry")
            continue
        board.resetSize(num_row, num_col)
        break
print("")
board.printBoard()

while menuChoice != "q":
    menuChoice = input("\n(menu \"m\"/quit \"q\") Select a row: ")

    if menuChoice == "m":
        menuChoice = input(""" 
    What would you like to do?
        p  print board
        r  reset
        s  save game
        l  load
        q  quit
    Anything else to continue: """)

        if menuChoice == "p":
            board.printBoard()
        elif menuChoice == "r":
            board.reset()
        elif menuChoice == "s":
            board.saveState()
        elif menuChoice == "l":
            board.loadState()
        continue

    if menuChoice == "q":
        break
    try: # handle user input
        row = int(menuChoice)
        col = int(input ("Select a collumn: "))
        if row < 1 or row > num_row or col < 1 or col > num_col:
            print("Out of range")
            continue
    except(TypeError, ValueError):
        print("Invalid entry")
        continue
    # run tile selection, check for success or failure
    checkLoss = board.selectTile(row, col)
    if checkLoss == True:
        print("You lost!")
        board.printBoard()
        break
    if board.checkSuccess() == True:
        print("You Won!")
        board.printBoard()
        break
    # show game state after change
    board.printBoard()


