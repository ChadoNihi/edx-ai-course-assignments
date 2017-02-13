from operator import itemgetter

from random import randint
from BaseAI import BaseAI_3

class PlayerAI(BaseAI):
    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        return max([(i, v) for i, v in moves], key=itemgetter(1))

    def minimax(self, grid, a, b, depth, isMaxPlayer):
        if timeout or tooDeep:
            return h(grid)
        elif isMaxPlayer:
            pass
        else:
            pass
