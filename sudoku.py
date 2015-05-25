import numpy as np

def loadPuzzle():
    f = open("/Users/Chris/myCode/sudoku_input.txt", "r")
    puzzle = []
    line = []
    row = []
    number = []

    for x in range(1,10):
        line = file.readline(f)
        row = []
        for y in range(0,18):
            if y%2 == 0:
                number = int(line[y])
                row.append(number)
        puzzle.append(row)
        
    return puzzle
    
    
def calculatePossibilities(puzzle, rowNum, colNum):
    
    listOfPoss = [1,2,3,4,5,6,7,8,9]
    
    subGrid0 = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
    subGrid1 = [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)]
    subGrid2 = [(0,6),(0,7),(0,8),(1,6),(1,7),(1,8),(2,6),(2,7),(2,8)]
    subGrid3 = [(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2)]
    subGrid4 = [(3,3),(3,4),(3,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5)]
    subGrid5 = [(3,6),(3,7),(3,8),(4,6),(4,7),(4,8),(5,6),(5,7),(5,8)]
    subGrid6 = [(6,0),(6,1),(6,2),(7,0),(7,1),(7,2),(8,0),(8,1),(8,2)]
    subGrid7 = [(6,3),(6,4),(6,5),(7,3),(7,4),(7,5),(8,3),(8,4),(8,5)]
    subGrid8 = [(6,6),(6,7),(6,8),(7,6),(7,7),(7,8),(8,6),(8,7),(8,8)]
    
    subGrids = [subGrid0,subGrid1,subGrid2,subGrid3,subGrid4,
                subGrid5,subGrid6,subGrid7,subGrid8]
    
    #eliminate row matches
    for x in range(0,9):
        for y in listOfPoss:
            if puzzle[rowNum][x] == y:
                listOfPoss.remove(y)
             
    #eliminate column matches   
    for x in range(0,9):
        for y in listOfPoss:
            if puzzle[x][colNum] == y:
                listOfPoss.remove(y)
    
    #find subgrid
    sifter = []
    i = 0
    
    while sifter == []:
        
        grid = subGrids[i]
        sifter = [element for element in grid 
                            if element[0] == rowNum and element[1] == colNum ]
                            
        i = i + 1
        
    locatedSubGridIndex = i - 1
    
    locatedSubGrid = subGrids[locatedSubGridIndex]
    
    #eliminate subgrid matches
    for x in range(0,9):
        gridX = locatedSubGrid[x][0]
        gridY = locatedSubGrid[x][1]
        for y in listOfPoss:
           if puzzle[gridX][gridY] == y:
                listOfPoss.remove(y)
    
    return listOfPoss    
    
#create a possibility matrix
def createPosMatrix(puzzle):

    n = 9
    possible = [[[0 for k in xrange(n)] for j in xrange(n)] for i in xrange(n)]

    for rowNum in range(0,9):
        row = puzzle[rowNum]
        for colNum in range(0,9):
            listOfPoss = []
	    if row[colNum] == 0:
                listOfPoss = calculatePossibilities(puzzle, rowNum, colNum)
                possible[rowNum][colNum] = listOfPoss
     
    return possible
    
def checkRules(puzzle):
    
    rulesBroken = False
    temp = []
    
    #check all rows
    
    for row in puzzle:
        temp = []
        for element in row:
            if element in temp and element != 0:
                rulesBroken = True
            else:
                temp.append(element)      
    
    
    #check all columns
    
    for column in range(0,9):
        temp = []
        for row in puzzle:
            if row[column] in temp and row[column] != 0:
                rulesBroken = True
            else:
                temp.append(row[column])
                

    #check all subgrids
    
    subGrid0 = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
    subGrid1 = [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)]
    subGrid2 = [(0,6),(0,7),(0,8),(1,6),(1,7),(1,8),(2,6),(2,7),(2,8)]
    subGrid3 = [(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2)]
    subGrid4 = [(3,3),(3,4),(3,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5)]
    subGrid5 = [(3,6),(3,7),(3,8),(4,6),(4,7),(4,8),(5,6),(5,7),(5,8)]
    subGrid6 = [(6,0),(6,1),(6,2),(7,0),(7,1),(7,2),(8,0),(8,1),(8,2)]
    subGrid7 = [(6,3),(6,4),(6,5),(7,3),(7,4),(7,5),(8,3),(8,4),(8,5)]
    subGrid8 = [(6,6),(6,7),(6,8),(7,6),(7,7),(7,8),(8,6),(8,7),(8,8)]
    
    subGrids = [subGrid0,subGrid1,subGrid2,subGrid3,subGrid4,
                subGrid5,subGrid6,subGrid7,subGrid8]
                
    for grid in subGrids:
        temp = []
        for x in range(0,9):
            
            gridX = grid[x][0]
            gridY = grid[x][1]

            if puzzle[gridX][gridY] != 0:
                if puzzle[gridX][gridY] in temp:
                    rulesBroken = True
                else:
                    temp.append(puzzle[gridX][gridY])

    return rulesBroken

def solver(puzzle, possible, rowNum, colNum):
    
    
    rulesBroken = False
    
    newRowNum = rowNum
    newColNum = colNum +1
    
    if rowNum == 9 and colNum == 0:
        print(np.matrix(puzzle))
        
    
    if newColNum == 9:
        newRowNum = rowNum + 1
        newColNum = 0
    
    if rowNum < 9:
        if puzzle[rowNum][colNum] == 0:
            for poss in possible[rowNum][colNum]:
                
                puzzle[rowNum][colNum] = poss
                
                rulesBroken = checkRules(puzzle)
                
                if rulesBroken == False:
                    solver(puzzle, possible, newRowNum, newColNum)
                
            puzzle[rowNum][colNum] = 0
        else:
            solver(puzzle, possible, newRowNum, newColNum)
        

#driver
puzzle = loadPuzzle()
possible = createPosMatrix(puzzle)

rowNum = 0
colNum = 0
solver(puzzle, possible,rowNum, colNum)



            



