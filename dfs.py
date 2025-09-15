import time
import copy
from build_game import *

possibleMoves = ((0, 1), (1, 0), (0, -1), (-1, 0))
timeLimit = 25


def depthFirstSearch(boardState):
    stack = [copy.deepcopy(boardState)]
    stateHist = []
    timeStart = time.time()

    while time.time() < timeStart + timeLimit:
        lastState = stack.pop()

        if check(lastState):
            print("Solved in", time.time() - timeStart, "secs")
            return lastState

        for step in possibleMoves:
            if isLegal(lastState, step) and not blocked(lastState, step):
                newState = copy.deepcopy(lastState)
                move(newState, step)

                if not searchHist(newState, stateHist):
                    stack.append(newState)
                    stateHist.append(newState)

    print("Time limit of", timeLimit, "secs exceeded")
    return boardState
