import time
import copy
from build_game import *

possibleMoves = ((0, 1), (1, 0), (0, -1), (-1, 0))
timeLimit = 180


def breadthFirstSearch(boardState):
    q = [copy.deepcopy(boardState)]
    stateHist = []
    timeStart = time.time()

    while time.time() < timeStart + timeLimit:
        lastState = q.pop(0)

        if check(lastState):  # Solution trouvée
            print("Solved in", time.time() - timeStart, "secs")
            return lastState

        for step in possibleMoves:
            if isLegal(lastState, step) and not blocked(lastState, step):
                newState = copy.deepcopy(lastState)
                move(newState, step)

                if not searchHist(newState, stateHist):
                    q.append(newState)
                    stateHist.append(newState)

    print("Time limit of", timeLimit, "secs exceeded")
    return boardState
