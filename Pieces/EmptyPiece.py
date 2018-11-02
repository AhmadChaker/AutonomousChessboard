from Pieces.Constants import PieceEnums
from Pieces.IBasePiece import IBasePiece
from Board.Constants import TeamEnum


class EmptyPiece(IBasePiece):

    def __init__(self, coords):
        IBasePiece.__init__( self, TeamEnum.NoTeam, coords)

    def GetPieceStr(self):
        return '-'

    def GetPieceEnum(self):
        return PieceEnums.Empty

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        return []
