from Board.Movement import Movement


class History:

    def __init__(self):
        self.__historicalMoves = []

    def AppendMovement(self, move: Movement):
        self.__historicalMoves.append(move)

    def GetHistoricalMoves(self):
        return self.__historicalMoves

    def GetLastMove(self):
        if len(self.__historicalMoves) != 0:
            return self.__historicalMoves[-1]
        return None
