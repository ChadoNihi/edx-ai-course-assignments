from math import inf
from operator import itemgetter
from random import random

from random import randint
from BaseAI import BaseAI_3

class PlayerAI(BaseAI):
    PROB_4 = 0
    TILL_DEPTH = 5

    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        v = -inf
        bestDir = None
        for dir in moves:
            nextGrid = grid.clone()
            nextGrid.move(dir)
            vCand = max(v, minimax(nextGrid, a, b, incredDepth, False))

            if vCand > v:
                v = vCand
                bestDir = dir
        return bestDir

    def minimax(self, grid, a, b, depth, isMaxPlayer=False):
        if timeout or depth == self.TILL_DEPTH:
            return h(grid)
        elif isMaxPlayer:
            incredDepth = depth + 1
            v = -inf
            moves = grid.getAvailableMoves()
            for dir in moves:
                nextGrid = grid.clone()
                nextGrid.move(dir)
                v = max(v, minimax(nextGrid, a, b, incredDepth, False))

                a = max(a, v)
                if b <= a: break
        else:
            incredDepth = depth + 1
            v = inf
            emptyCells = grid.getAvailableCells() #what order promotes early pruning?
            for cell in emptyCells:
                nextGrid = grid.clone()
                nextGrid.insertTile(cell, 2 if random() < self.PROB_4 else 4)
                v = min(v, minimax(nextGrid, a, b, incredDepth, True))

                b = min(b, v)
                if b <= a: break
            return v
