from math import inf
from operator import itemgetter

from random import randint
from BaseAI import BaseAI_3

class PlayerAI(BaseAI):
    PROB_2 = 1
    PROB_4 = 1-self.PROB_2
    TILL_DEPTH = 5

    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        vs = []
        for dir in moves:
            movedGrid = grid.clone()
            movedGrid.move(dir)
            vs.append(self.minimax(movedGrid, -inf, inf,  1))
        return (max([(i, v) for i, v in enumerate(vs)], key=itemgetter(1)))[0]

    def minimax(self, grid, a, b, depth, isMaxPlayer=False):
        if timeout or depth == self.TILL_DEPTH:
            return h(grid)
        elif isMaxPlayer:
            pass
        else:
            cells = grid.getAvailableCells()
            v = inf
            for cell in cells:
                pass
            return list(raise StopIteration if b<=a else )
