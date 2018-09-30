from abc import ABC, abstractmethod


class IBasePiece(ABC):

    def __init__(self, team, coordinates):
        self.__team = team
        self.__coordinates = coordinates
        # Record history of each move, keep appending to vector
        # self.__history =

    @abstractmethod
    def GetPieceStr(self):
        pass

    @abstractmethod
    def GetPieceEnum(self):
        pass

    @abstractmethod
    def CanMove(self, chessBoard):
        pass

    @abstractmethod
    def Move(self, chessBoard):
        pass

    def GetTeam(self):
        return self.__team

    def GetCoordinates(self):
        return self.__coordinates



