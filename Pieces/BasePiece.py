from abc import ABC, abstractmethod


class IBasePiece(ABC):

    def __init__(self, team):
        self.__team = team
        # Record history of each move, keep appending to vector
        # self.__history =

    @abstractmethod
    def GetPieceStr(self):
        pass

    @abstractmethod
    def GetPieceEnum(self):
        pass


    def GetTeam(self):
        return self.__team



