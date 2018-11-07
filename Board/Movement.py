from Miscellaneous.Points import Points
from Pieces.Constants import PieceEnums


class Movement:

    def __init__(self, pieceAtFromCoord, pieceAtToCoord, fromCoord: Points, toCoord: Points, isEnPassantMove):
        self.__pieceEnumFromCoord = pieceAtFromCoord.GetPieceEnum()
        self.__pieceEnumToCoord = pieceAtToCoord.GetPieceEnum()
        self.__teamMoved = pieceAtFromCoord.GetTeam()
        self.__fromCoord = fromCoord
        self.__toCoord = toCoord
        self.__isCaptureMove = True if (self.__pieceEnumToCoord != PieceEnums.Empty or isEnPassantMove) else False

    def __eq__(self, other):
        return self.__pieceEnumFromCoord == other.__pieceEnumFromCoord and \
               self.__pieceEnumToCoord == other.__pieceEnumToCoord and \
               self.__fromCoord == other.__fromCoord and \
               self.__toCoord == other.__toCoord and \
               self.__teamMoved == other.__teamMoved and \
               self.__isCaptureMove == other.__isCaptureMove

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

    def GetXMovement(self):
        return abs(self.GetFromCoord().GetX() - self.GetToCoord().GetX())

    def GetYMovement(self):
        return abs(self.GetFromCoord().GetY() - self.GetToCoord().GetY())
