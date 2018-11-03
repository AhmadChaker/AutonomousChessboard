from Utilities.Points import Points
from Pieces.Constants import PieceEnums
from Pieces.IBasePiece import IBasePiece


class Movement:

    def __init__(self, pieceAtFromCoord: IBasePiece, pieceAtToCoord: IBasePiece, fromCoord: Points, toCoord: Points):
        self.__pieceEnumFromCoord = pieceAtFromCoord.GetPieceEnum()
        self.__pieceEnumToCoord = pieceAtToCoord.GetPieceEnum()
        self.__teamMoved = pieceAtFromCoord.GetTeam()
        self.__fromCoord = fromCoord
        self.__toCoord = toCoord

        self.__isCaptureMove = True if self.__pieceEnumToCoord != PieceEnums.Empty else False

    def __eq__(self, other):
        return self.__pieceEnumFromCoord == other.__pieceEnumFromCoord and \
               self.__pieceEnumToCoord == other.__pieceEnumToCoord and \
               self.__fromCoord == other.__pieceFromCoord and \
               self.__toCoord == other.__toCoord and \
               self.__teamMoved == other.__teamMoved

    def IsCaptureMove(self):
        return self.__isCaptureMove

    def GetPieceEnumFrom(self):
        return self.__pieceEnumFromCoord

    def GetPieceEnumTo(self):
        return self.__pieceEnumToCoord

    def GetFromCoord(self):
        return self.__fromCoord

    def GetTeamMoved(self):
        return self.__teamMoved

    def GetToCoord(self):
        return self.__toCoord
