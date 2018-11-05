import Utilities.Points
from Board.Movement import Movement
from abc import ABC, abstractmethod


class IBasePiece(ABC):

    def __init__(self, team, coordinates:Utilities.Points.Points):
        self.__team = team
        self.__coordinates = coordinates
        self.__history = [coordinates]

    @abstractmethod
    def GetPieceStr(self):
        pass

    @abstractmethod
    def GetPieceEnum(self):
        pass

    @abstractmethod
    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        pass

    def CanMove(self, board, toMovePoint:Utilities.Points.Points, lastMove:Movement):

        if toMovePoint == Utilities.Points.POINTS_UNDEFINED:
            return False

        enforceKingUnderAttackCheck = True
        validMoves = self.GetValidMoves(board, enforceKingUnderAttackCheck)
        if len(validMoves) == 0:
            return False

        canMove = any(move == toMovePoint for move in validMoves)
        return canMove

    def Move(self, board, toMovePoint:Utilities.Points.Points, lastMove:Movement):

        if not self.CanMove(board, toMovePoint, lastMove):
            return False

        self.SetCoordinates(toMovePoint)
        return True

    # Force move with no CanMove check
    def ForceMove(self, toMovePoint:Utilities.Points.Points):
        self.SetCoordinates(toMovePoint)
        return True

    # Force move with no CanMove check and no addition to history
    def ForceMoveNoHistory(self, toMovePoint:Utilities.Points.Points):
        self.__coordinates = toMovePoint
        return True

    def GetTeam(self):
        return self.__team

    def SetCoordinates(self, newCoords):
        self.__coordinates = newCoords
        self.__history.append(newCoords)

    def GetCoordinates(self):
        return self.__coordinates

    def GetHistory(self):
        return self.__history



