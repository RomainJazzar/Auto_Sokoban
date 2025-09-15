def printf(obj):
    for i in range(0, len(obj.matrix)):
        for j in range(0, len(obj.matrix[0])):
            if(i == obj.playerY and j == obj.playerX):
                print("@", end = '')
            else:
                print(obj.matrix[i][j], end = '')
        print()
    print("")

def check(currLevel):
    clear = True
    for i in range(0, currLevel.rows):
        for j in range(0, currLevel.cols):
            if currLevel.matrix[i][j] == 2:
                clear = False
    return clear
 
def move(levelObj, vals):
    newY = levelObj.playerY + vals[1]
    newX = levelObj.playerX + vals[0]
    nextY = levelObj.playerY + 2 * vals[1]
    nextX = levelObj.playerX + 2 * vals[0]
    debug = False
    # Vérifie que les indices sont valides
    if 0 <= newY < levelObj.rows and 0 <= newX < levelObj.cols:
        target = levelObj.matrix[newY][newX]

        if target == 0 or target == 2:
            levelObj.playerY = newY
            levelObj.playerX = newX
            levelObj.timeLine.append(vals)
        else:
            # Vérifie que la destination pour pousser est aussi dans les limites
            if 0 <= nextY < levelObj.rows and 0 <= nextX < levelObj.cols:
                levelObj.matrix[newY][newX] -= 3
                levelObj.matrix[nextY][nextX] += 3
                levelObj.playerY = newY
                levelObj.playerX = newX
                levelObj.timeLine.append(vals)
            else:
                print("Erreur: tentative de pousser une caisse hors de la grille.")
    else:
        if debug:
            print("Erreur: tentative de pousser une caisse hors de la grille.")

def isLegal(currLevel, vals):
    y = currLevel.playerY + vals[1]
    x = currLevel.playerX + vals[0]
    yy = currLevel.playerY + 2 * vals[1]
    xx = currLevel.playerX + 2 * vals[0]

    if not (0 <= y < currLevel.rows and 0 <= x < currLevel.cols):
        return False

    if currLevel.matrix[y][x] == 1:
        return False
    elif currLevel.matrix[y][x] in (0, 2):
        return True
    elif (0 <= yy < currLevel.rows and 0 <= xx < currLevel.cols and
          currLevel.matrix[yy][xx] != 1 and currLevel.matrix[yy][xx] < 3):
        return True
    return False

def blocked(currLevel, vals):
    if currLevel.matrix[currLevel.playerY+vals[1]][currLevel.playerX+vals[0]] == 3 and currLevel.matrix[currLevel.playerY+2*vals[1]][currLevel.playerX+2*vals[0]] != 2:
        if(currLevel.matrix[currLevel.playerY+2*vals[1]+1][currLevel.playerX+2*vals[0]] == 1 and currLevel.matrix[currLevel.playerY+2*vals[1]][currLevel.playerX+2*vals[0]+1] == 1):
            return True
        elif(currLevel.matrix[currLevel.playerY+2*vals[1]+1][currLevel.playerX+2*vals[0]] == 1 and currLevel.matrix[currLevel.playerY+2*vals[1]][currLevel.playerX+2*vals[0]-1] == 1):
            return True    
        elif(currLevel.matrix[currLevel.playerY+2*vals[1]-1][currLevel.playerX+2*vals[0]] == 1 and currLevel.matrix[currLevel.playerY+2*vals[1]][currLevel.playerX+2*vals[0]+1] == 1):
            return True   
        elif(currLevel.matrix[currLevel.playerY+2*vals[1]-1][currLevel.playerX+2*vals[0]] == 1 and currLevel.matrix[currLevel.playerY+2*vals[1]][currLevel.playerX+2*vals[0]-1] == 1):
            return True  
    return False

def searchHist(gameState, hist):
    for item in hist:
        if item.matrix == gameState.matrix:
            if(item.playerY == gameState.playerY and item.playerX == gameState.playerX):
                return True
    return False

def moveDictation(moves):
    moveNames = {(1, 0): "Right", (-1, 0): "Left", (0, 1): "Down", (0, -1): "Up"}
    for item in moves:
        print(moveNames[item], end = "=>")

def wallFreeFaces(matrix, pos):
    res = []
    if pos[0] > 0 and matrix[pos[0]-1][pos[1]] not in (1, 6):
        res.append((-1, 0))
    if pos[0] < len(matrix)-1 and (matrix[pos[0]+1][pos[1]]) not in (1, 6):
        res.append((1, 0))
    if pos[1] > 0 and matrix[pos[0]][pos[1]-1] not in (1, 6):
        res.append((0, -1))
    if pos[1] < len(matrix[0])-1 and matrix[pos[0]][pos[1]+1] not in (1, 6):
        res.append((0, 1))
    return res

def manhattanDist(gameState, boxPos):                               #Manhattan distances between all the possible 
    dist = []                                                       #destinations and the current box
    for i in range(0, gameState.rows):
        for j in range(0, gameState.cols):
            if gameState.matrix[i][j] == 2:
                dist.append(abs(boxPos[0]-i)+abs(boxPos[1]-j))
    return dist