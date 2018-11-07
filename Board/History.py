from Board.Movement import Movement


class History:

    def __init__(self):
        self.__historicalMoves = []

    def __eq__(self, other):
        firstHistMoves = self.GetHistoricalMoves()
        otherHistMoves = other.GetHistoricalMoves()
        if len(firstHistMoves) != len(otherHistMoves):
            return False

        for index in range(len(firstHistMoves)):
            if firstHistMoves[index] != otherHistMoves[index]:
                return False

        return True

    def AppendMovement(self, move: Movement):
        self.__historicalMoves.append(move)

    def GetHistoricalMoves(self):
        return self.__historicalMoves

    def GetLastMove(self):
        if len(self.__historicalMoves) != 0:
            return self.__historicalMoves[-1]
        return None
