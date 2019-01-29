import logging
import math
from Board.Movement import Movement


logger = logging.getLogger(__name__)


class History:

    def __init__(self):
        self.__historicalMoves = []
        self.__turns = 0

    def __eq__(self, other):
        firstHistMoves = self.GetHistoricalMoves()
        otherHistMoves = other.GetHistoricalMoves()
        if len(firstHistMoves) != len(otherHistMoves):
            return False

        for index in range(len(firstHistMoves)):
            if firstHistMoves[index] != otherHistMoves[index]:
                return False

        return True

    def Clear(self):
        self.__historicalMoves.clear()
        self.__turns = 0

    def AppendMovement(self, move: Movement):
        self.__historicalMoves.append(move)

        # There are two moves for a castle, the first is a king move (can only be done in a castle),
        # The second is the rook move (not classified as a castle move per se). Since it's the same team we only increase
        # by 0.5 at a time
        if not move.IsCastleMove():
            self.__turns += 0.5

    def GetHistoricalMoves(self):
        return self.__historicalMoves

    def GetLastMove(self):
        if len(self.__historicalMoves) != 0:
            return self.__historicalMoves[-1]
        return None

    def PrintHistory(self):
        for historicalMove in self.GetHistoricalMoves():
            logger.info(historicalMove.ToString())

    def GetNumberofTurns(self):
        return math.floor(self.__turns)
