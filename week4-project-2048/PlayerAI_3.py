from math import inf
from operator import itemgetter
from random import random
from time import perf_counter

from random import randint
from BaseAI import BaseAI_3

class PlayerAI(BaseAI):
    EMPTY_CELL_BONUS = 1
    GRID_SZ = 4
    PROB_4 = 0
    TILL_DEPTH = 5
    TIME_LIMIT = 0.1

    def getMove(self, grid):
        startT = perf_counter()
        moves = grid.getAvailableMoves()
        v = -inf
        bestDir = None
        for dir in moves:
            nextGrid = grid.clone()
            nextGrid.move(dir)
            vCand = max(v, self.minimax(nextGrid, a, b, 1, startT, False))

            if vCand > v:
                v = vCand
                bestDir = dir

        return bestDir

    def minimax(self, grid, a, b, depth, startT, isMaxPlayer=False):
        if perf_counter()-startT >= self.TIME_LIMIT or depth >= self.TILL_DEPTH or not grid.canMove():
            return self.h(grid)
        elif isMaxPlayer:
            incredDepth = depth + 1
            v = -inf
            moves = grid.getAvailableMoves()
            for dir in moves:
                nextGrid = grid.clone()
                nextGrid.move(dir)
                v = max(v, self.minimax(nextGrid, a, b, incredDepth, startT, False))

                a = max(a, v)
                if b <= a: break

            return v
        else:
            incredDepth = depth + 1
            v = inf
            emptyCells = grid.getAvailableCells() #what order promotes early pruning?
            for cell in emptyCells:
                nextGrid = grid.clone()
                nextGrid.insertTile(cell, 2 if random() < self.PROB_4 else 4)
                v = min(v, self.minimax(nextGrid, a, b, incredDepth, startT, True))

                b = min(b, v)
                if b <= a: break

            return v

    def h(grid):
        numOfEmptyCells = 0
        for x in range(self.GRID_SZ):
            for y in range(self.GRID_SZ):
                if not grid.map[x][y]: numOfEmptyCells += 1

        if not numOfEmptyCells:
            return -inf

        return (self.monotone_triangle_h(grid)
                + max(self.hor_adjac_h(grid), self.vert_adjac_h(grid))
                # + self.smoothness_h(grid)
                + self.EMPTY_CELL_BONUS*(numOfEmptyCells-1))

    def monotone_triangle_h(grid):
        pass
