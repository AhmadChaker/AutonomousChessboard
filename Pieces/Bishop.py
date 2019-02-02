import sys
import Miscellaneous.Constants
from Miscellaneous.Constants import PieceEnums, TeamEnum
from Miscellaneous.Points import Points
from Utilities.MoveHelpers import MoveHelpers
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class Bishop(IBasePiece):

    WhitePieceString = u'\u2657'
    BlackPieceString = u'\u265D'
    WhitePieceFenString = 'B'
    BlackPieceFenString = 'b'
    MoveIterations = sys.maxsize

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == TeamEnum.White:
            return Bishop.WhitePieceString
        elif team == TeamEnum.Black:
            return Bishop.BlackPieceString

        return Miscellaneous.Constants.BOARD_ERROR_STRING

    def GetFenRepresentation(self):
        team = self.GetTeam()
        if team == TeamEnum.White:
            return Bishop.WhitePieceFenString
        elif team == TeamEnum.Black:
            return Bishop.BlackPieceFenString

        return Miscellaneous.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return PieceEnums.Bishop

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        validMoves = []
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(1, 1), Bishop.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(1, -1), Bishop.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-1, 1), Bishop.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-1, -1), Bishop.MoveIterations, enforceKingUnderAttackCheck))
        return validMoves
