from Board.Movement import Movement
from Board.Constants import TeamEnum
from Pieces.Constants import PieceEnums


class History:

    def __init__(self):
        self.__historicalMoves = []
        self.__hasWhiteCastled = False
        self.__hasBlackCastled = False

    def AppendMovement(self, move: Movement):
        self.__historicalMoves.append(move)

        # Only need to check if King has moved two spaces in x direction to determine castling

    def GetHistoricalMoves(self):
        return self.__historicalMoves

    def HasCastled(self, team: TeamEnum):
        if team == TeamEnum.White:
            if self.__hasWhiteCastled:
                return True

        if team == TeamEnum.Black:
            if self.__hasBlackCastled:
                return True

        # Go through historical moves and see if King has moved
        for historicalMove in self.__historicalMoves:
            if historicalMove.GetPieceEnumFrom() == PieceEnums.King:
                difference = abs(historicalMove.GetFromCoord().GetX() - historicalMove.GetToCoord().GetX())
                if difference > 1:
                    if team == TeamEnum.White:
                        self.__hasWhiteCastled = True
                    else:
                        self.__hasBlackCastled = True
                    return True
        return False
