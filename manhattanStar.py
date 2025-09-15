from queue import PriorityQueue
import time
import copy
from build_game import *

possibleMoves = ((0, 1), (1, 0), (0, -1), (-1, 0))
timeLimit = 32

def aStarManhattan(gameState):
    pq = PriorityQueue()
    stateHist = []

    # Fonction heuristique locale
    def heuristic(state):
        hx = 0
        for i in range(state.rows):
            for j in range(state.cols):
                if state.matrix[i][j] == 3:  # Box not yet on goal
                    hx += min(manhattanDist(state, (i, j)))
        return hx

    pq.put((heuristic(gameState), id(gameState), gameState))
    timeStart = time.time()

    while time.time() < timeStart + timeLimit:
        _, _, lastState = pq.get()

        if check(lastState):
            print("Solved in", time.time() - timeStart, "secs")
            return lastState

        for step in possibleMoves:
            if isLegal(lastState, step) and not blocked(lastState, step):
                newState = copy.deepcopy(lastState)
                move(newState, step)

                if not searchHist(newState, stateHist):
                    score = heuristic(newState)
                    pq.put((score + len(newState.timeLine), id(newState), newState))
                    stateHist.append(newState)

    print("Time limit of", timeLimit, "secs exceeded")
    return gameState
