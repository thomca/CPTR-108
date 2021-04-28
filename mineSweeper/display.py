import random
import os

class Board:
    boardArray = list()
    loss = False
    win = False
    ROWS = 6
    COLS = 8

    def __init__(self, row, col):
        """
        Intializes grid
        :param row: int.
        :param col: int.
        """
        self.resetSize(row, col)

    def printBoard(self):
        """
        prints board using class ROWS and COLS
        to determine size and boardArray for tile list
        """
        # label for columns
        print(" ", end=" ")
        for z in range(1, (self.COLS + 1)):
            if z >= 9:
                print(" ", z ,end="")
            else:
                print(" ", z ,end=" ")
        print(" ")
        # print rows
        row = 0
        while row < self.ROWS:
            col = 0
            # labels
            if row >= 9:
                print(row + 1, end="")
            else:
                print(row + 1, end=" ")
            # contents printed, hide mines unless win or loss
            while col < self.COLS:
                if self.loss == False and self.win == False and self.boardArray[row][col] == "m":
                    print("|","-",end=" ")
                else:
                    print("|", self.boardArray[row][col], end=" ")
                col = col + 1
            row = row + 1
            print("|")

    def resetSize(self, row, col):
        """
        Changes grid size and resets mines
        :param row: int.
        :param col: int.
        """
        self.ROWS = row
        self.COLS = col
        self.reset()


    def reset(self):
        """
        Sets up grid based on ROWS and COLS
        mines set based on 10% of total 
        """
        self.boardArray.clear()
        self.boardArray = [ ["-" for i in range (self.COLS) ] for j in range(self.ROWS) ]
        self.loss = False
        self.win = False
        mineCount = 0
        mines = list()
        while mineCount < (self.ROWS * self.COLS)/10:
            row = random.randint(0,self.ROWS-1)
            col = random.randint(0,self.COLS-1)
            if [row,col] not in mines:
                mines.append([row,col])
                self.boardArray[row][col] = "m"
                mineCount = mineCount + 1

    def checkSuccess(self):
        """
        If all tiles (excluding mines) have been
        explored, then you win
        :param return: bool win, False to continue
        """
        self.win = True
        row = 0
        while row < self.ROWS:
            col = 0
            while col < self.COLS:
                if self.boardArray[row][col] == "-":
                    self.win = False
                    break
                col = col + 1
            if self.win == False:
                break
            row = row + 1
        return self.win

    def selectTile(self, row, col):
        """
        Selects a tile at index row-1, col-1
        If it is a mine then you lose, otherwise
        surrounding tiles are iterated through in 
        search of mines until tiles in the area 
        without near by mines are left blank and 
        tiles that touch mines are labeled with how
        many they touch.
        :param row: int.
        :param col: int.
        :param return: bool loss, False if continue
        """
        currentRow = row - 1
        currentCol = col - 1
        # check for loss
        if self.boardArray[currentRow][currentCol] == "m":
            self.loss = True
        else:
            # track tiles to vist in tilesToCheck, start with current
            tilesToCheck = list()
            tilesToCheck.append([currentRow,currentCol])

            while len(tilesToCheck) != 0:
                currentRow = tilesToCheck[0][0]
                currentCol = tilesToCheck[0][1]
                tilesToCheck.pop(0) # remove first item
                self.boardArray[currentRow][currentCol] = " "

                # check for mines, if none iteratively check all sides 
                mine_count = 0
                for x in range(-1,2):
                    for y in range(-1,2):
                        if (currentRow + x) >= 0 and (currentCol + y) >= 0 and (currentRow + x) < self.ROWS and (currentCol + y) < self.COLS:
                            if self.boardArray[currentRow + x][currentCol + y] == "m":
                                mine_count = mine_count + 1

                if mine_count == 0:
                    # add new tiles to be checked
                    for x in range(-1,2):
                        for y in range(-1,2):
                            if (currentRow + x) >= 0 and (currentCol + y) >= 0 and (currentRow + x) < self.ROWS and (currentCol + y) < self.COLS and not (x == 0 and y == 0):
                                if self.boardArray[currentRow + x][currentCol + y] == "-" and [currentRow + x, currentCol + y] not in tilesToCheck:
                                    tilesToCheck.append([currentRow + x, currentCol + y])
                else:
                    self.boardArray[currentRow][currentCol] = str(mine_count)
            
        return self.loss

    def saveState(self):
        # save to savegame.txt
        with open("mineSweeper/savegame.txt", "w") as f:
            f.write(str(self.ROWS) + " " + str(self.COLS) + "\n")
            for x in range(0,self.ROWS):
                for y in range(0,self.COLS):
                    f.write(self.boardArray[x][y])

    def loadState(self):
        # load savegame.txt
        filePath = "mineSweeper/savegame.txt"
        if os.path.isfile(filePath):
            sizeString = ""
            info = ""
            with open(filePath, "r") as f:
                sizeString = f.readline()
                info = f.readline()
            sizeList = sizeString.split()
            rows = int(sizeList[0])
            cols = int(sizeList[1])
            self.resetSize (rows, cols)
            i = 0
            for x in range(0,rows):
                    for y in range(0,cols):
                        self.boardArray[x][y] = info[i]
                        i = i + 1
            return True
        else:
            print("No file exists")
            return False
        