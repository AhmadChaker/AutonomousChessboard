import Utilities.Points
from abc import ABC, abstractmethod


class IBasePiece(ABC):

    def __init__(self, team, coordinates):
        self.__team = team
        self.__coordinates = coordinates
        self.__history = []

    @abstractmethod
    def GetPieceStr(self):
        pass

    @abstractmethod
    def GetPieceEnum(self):
        pass

    @abstractmethod
    def GetValidMoves(self, board):
        pass

    def CanMove(self, toMovePoint:Utilities.Points.Points):

        if toMovePoint == Utilities.Points.POINTS_UNDEFINED:
            return False

        validMoves = self.GetValidMoves()
        if len(validMoves) == 0:
            return False

        canMove = any(move == toMovePoint for move in validMoves)
        return canMove

    def Move(self, toMovePoint:Utilities.Points.Points):

        if not self.CanMove(toMovePoint):
            return False

        self.SetCoordinates(toMovePoint)
        return True

    def ForceMove(self, toMovePoint:Utilities.Points.Points):
        self.SetCoordinates(toMovePoint)
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



