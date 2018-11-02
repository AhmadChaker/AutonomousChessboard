from Board.Movement import Movement


class History:

    def __init__(self):
        self.__historicalMoves = []

    def AppendMovement(self, move: Movement):
        self.__historicalMoves.append(move)

    def GetHistoricalMoves(self):
        return self.__historicalMoves
