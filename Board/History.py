from Utilities.Points import Points
from Pieces.Constants import PieceEnums


class History:

    def __init__(self, pieceAtFromCoord: PieceEnums, pieceAtToCoord: PieceEnums, fromCoord: Points, toCoord: Points):
        self.__pieceFromCoord = pieceAtFromCoord
        self.__pieceAtToCoord = pieceAtToCoord
        self.__fromCoord = fromCoord
        self.__toCoord = toCoord

        self.__isCaptureMove = False if self.__pieceAtToCoord == PieceEnums.Empty else True

    def __eq__(self, other):
        return self.__pieceFromCoord == other.__pieceFromCoord and self.__pieceAtToCoord == other.__pieceAtToCoord and \
               self.__fromCoord == other.__pieceFromCoord and self.__toCoord == other.__toCoord

    def IsCaptureMove(self):
        return self.__isCaptureMove

    def GetPieceFrom(self):
        return self.__pieceFromCoord

    def GetPieceAtTo(self):
        return self.__pieceAtToCoord

    def GetFromCoord(self):
        return self.__fromCoord

    def GetToCoord(self):
        return self.__toCoord
