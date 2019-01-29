from Miscellaneous.Constants import PieceEnums, TeamEnum
from Pieces.IBasePiece import IBasePiece


class NoPiece(IBasePiece):

    def __init__(self, coords):
        IBasePiece.__init__( self, TeamEnum.NoTeam, coords)

    def GetPieceStr(self):
        # Unicode dash character to match width of chess pieces in unicode
        return '\u2015'

    def GetFenRepresentation(self):
        return ''

    def GetPieceEnum(self):
        return PieceEnums.NoPiece

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        return []
