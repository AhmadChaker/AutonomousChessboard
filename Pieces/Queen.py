import sys
import Miscellaneous.Constants
from Miscellaneous.Constants import TeamEnum, PieceEnums
from Miscellaneous.Points import Points
from Utilities.MoveHelpers import MoveHelpers
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class Queen(IBasePiece):

    WhitePieceString = u'\u2655'
    BlackPieceString = u'\u265B'
    WhitePieceFenString = 'Q'
    BlackPieceFenString = 'q'
    MoveIterations = sys.maxsize

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == TeamEnum.White:
            return Queen.WhitePieceString
        elif team == TeamEnum.Black:
            return Queen.BlackPieceString

        return Miscellaneous.Constants.BOARD_ERROR_STRING

    def GetFenRepresentation(self):
        team = self.GetTeam()
        if team == TeamEnum.White:
            return Queen.WhitePieceFenString
        elif team == TeamEnum.Black:
            return Queen.BlackPieceFenString

        return Miscellaneous.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return PieceEnums.Queen

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        validMoves = []
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(1, 1), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(1, 0), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(1, -1), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(0, -1), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-1, -1), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-1, 0), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-1, 1), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(0, 1), Queen.MoveIterations, enforceKingUnderAttackCheck))
        return validMoves
