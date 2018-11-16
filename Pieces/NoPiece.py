from Pieces.Constants import PieceEnums
from Pieces.IBasePiece import IBasePiece
from Board.Constants import TeamEnum


class NoPiece(IBasePiece):

    def __init__(self, coords):
        IBasePiece.__init__( self, TeamEnum.NoTeam, coords)

    def GetPieceStr(self):
        return '\u2015'

    def GetPieceEnum(self):
        return PieceEnums.NoPiece

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        return []
