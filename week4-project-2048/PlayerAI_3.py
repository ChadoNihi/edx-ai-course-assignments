#from math import inf
from math import sqrt
from operator import itemgetter
from random import random
from time import perf_counter

from BaseAI_3 import BaseAI

inf = 999999

(UP, DOWN, LEFT, RIGHT) = range(4)

class PlayerAI(BaseAI):
    GRID_SZ = 4
    PROB_4 = 0
    TILL_DEPTH = 4
    TIME_LIMIT = 0.1
    WEIGHTS = {'empty_cell_bonus': 3, 'maxVal': 0.06, 'max_val_is_in_corner': 35, 'merge_potential': 5}

    def getMove(self, grid):
        startT = perf_counter()
        moves = grid.getAvailableMoves()
        v = -inf-1
        bestDir = None
        for dir in moves:
            nextGrid = grid.clone()
            nextGrid.move(dir)
            vCand = max(v, self.minimax(nextGrid, -inf, inf, 1, startT, False))

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

    def h(self, grid):
        numOfEmptyCells = self.countEmptyCells(grid)

        if not numOfEmptyCells:
            return -inf

        # maxVal, pos, nextMaxVal, posNext = self.get_two_max_vals_w_pos(grid)
        # maxValsCloseness = 1 if (nextMaxVal and maxVal / nextMaxVal <= 8) and abs(pos[0]-posNext[0])<=1 and abs(pos[1]-posNext[1])<=1 else 0

        maxVal = grid.getMaxTile()
        maxValInCorner = 1 if grid.map[0][0]==maxVal or grid.map[0][-1]==maxVal or grid.map[-1][0]==maxVal or grid.map[-1][-1]==maxVal else 0

        return (maxValInCorner * self.WEIGHTS['max_val_is_in_corner']
                + maxVal * self.WEIGHTS['maxVal']
                + max(self.merge_potential_h(grid, LEFT, RIGHT), self.merge_potential_h(grid, UP, DOWN)) * self.WEIGHTS['merge_potential']
                + (numOfEmptyCells-1) * self.WEIGHTS['empty_cell_bonus'])

    # def monotone_triangle_h(self, grid):
    #     score = 0
    #
    #     return score

    # def get_two_max_vals_w_pos(self, grid):
    #     maxVal = -inf
    #     nextMaxVal = maxVal+1
    #     pos, posNext = None, None
    #
    #     for r, row in enumerate(grid.map):
    #         for c, val in enumerate(row):
    #             if val > maxVal:
    #                 maxVal, nextMaxVal = val, maxVal
    #                 pos, posNext = (r,c), pos
    #             elif val > nextMaxVal:
    #                 nextMaxVal = val
    #                 posNext = (r,c)

        return maxVal, pos, nextMaxVal, posNext

    def merge_potential_h(self, grid, dir, dirOpp):
        movedGrid = grid.clone()
        numOfEmptyCellsBeforeMove = self.countEmptyCells(movedGrid)

        movedGrid.move(dir)
        numOfEmptyCellsAFTERMove = self.countEmptyCells(movedGrid)

        movedGrid = grid.clone()
        movedGrid.move(dirOpp)

        return max(numOfEmptyCellsAFTERMove - numOfEmptyCellsBeforeMove,
                    self.countEmptyCells(movedGrid) - numOfEmptyCellsBeforeMove)

    def countEmptyCells(self, grid):
        numOfEmptyCells = 0
        for row in grid.map:
            for val in row:
                if not val: numOfEmptyCells += 1

        return numOfEmptyCells
