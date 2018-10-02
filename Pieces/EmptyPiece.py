from Pieces.Constants import PieceEnums
from Pieces.IBasePiece import IBasePiece


class EmptyPiece(IBasePiece):

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        return "-"

    def GetPieceEnum(self):
        return PieceEnums.Empty

    def GetValidMoves(self, chessBoard):
        return []
