import Miscellaneous.Constants
from Miscellaneous.Constants import TeamEnum, PieceEnums
from Miscellaneous.Points import Points
from Utilities.MoveHelpers import MoveHelpers
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class Knight(IBasePiece):

    WhitePieceString = u'\u2658'
    BlackPieceString = u'\u265E'
    WhitePieceFenString = 'N'
    BlackPieceFenString = 'n'
    MoveIterations = 1

    def __init__(self, team, coords):
        IBasePiece.__init__(self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == TeamEnum.White:
            return Knight.WhitePieceString
        elif team == TeamEnum.Black:
            return Knight.BlackPieceString

        return Miscellaneous.Constants.BOARD_ERROR_STRING

    def GetFenRepresentation(self):
        team = self.GetTeam()
        if team == TeamEnum.White:
            return Knight.WhitePieceFenString
        elif team == TeamEnum.Black:
            return Knight.BlackPieceFenString

        return Miscellaneous.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return PieceEnums.Knight

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        validMoves = []
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(2, 1), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(1, 2), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-1, 2), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-2, 1), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-2, -1), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-1, -2), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(1, -2), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(2, -1), Knight.MoveIterations, enforceKingUnderAttackCheck))
        return validMoves
