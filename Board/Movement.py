from Miscellaneous.BoardPoints import BoardPoints
from Pieces.Constants import PieceEnums
from Utilities.MoveHelpers import MoveHelpers


class Movement:

    def __init__(self, teamMoving, pieceAtFromCoord, pieceAtToCoord, fromCoord: BoardPoints, toCoord: BoardPoints, lastMove):
        self.__pieceEnumFromCoord = pieceAtFromCoord
        self.__pieceEnumToCoord = pieceAtToCoord
        self.__teamMoved = teamMoving
        self.__fromCoord = fromCoord
        self.__toCoord = toCoord

        self.__isCaptureMove = True if self.__pieceEnumToCoord != PieceEnums.NoPiece else False
        self.__isEnPassantMove = True if lastMove is not None and MoveHelpers.IsEnPassantMove(pieceAtFromCoord, fromCoord, toCoord, lastMove) else False
        if self.__isEnPassantMove:
            self.__isCaptureMove = True

        castleMove = MoveHelpers.IsCastleMove(pieceAtFromCoord, fromCoord, toCoord)
        self.__isCastleMove = MoveHelpers.IsCastleMove(pieceAtFromCoord, fromCoord, toCoord)

    def __eq__(self, other):
        return self.__pieceEnumFromCoord == other.__pieceEnumFromCoord and \
               self.__pieceEnumToCoord == other.__pieceEnumToCoord and \
               self.__fromCoord == other.__fromCoord and \
               self.__toCoord == other.__toCoord and \
               self.__teamMoved == other.__teamMoved and \
               self.__isCaptureMove == other.__isCaptureMove and \
               self.__isCastleMove == other.__isCastleMove and \
               self.__isEnPassantMove == other.__isEnPassantMove

    def IsCaptureMove(self):
        return self.__isCaptureMove

    def IsEnPassantMove(self):
        return self.__isEnPassantMove

    def IsCastleMove(self):
        return self.__isCastleMove

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
