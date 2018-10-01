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
    def CanMove(self):
        pass

    @abstractmethod
    def Move(self):
        pass

    @abstractmethod
    def GetValidMoves(self):
        pass

    def GetTeam(self):
        return self.__team

    def GetCoordinates(self):
        return self.__coordinates

    def GetHistory(self):
        return self.__history


