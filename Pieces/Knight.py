import Board.Constants
import Pieces.Constants
from Miscellaneous.Points import Points
from Utilities.BoardHelpers import BoardHelpers
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class Knight(IBasePiece):

    WhiteString = u'\u2658'
    BlackString = u'\u265E'
    MoveIterations = 1

    def __init__(self, team, coords):
        IBasePiece.__init__(self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Board.Constants.TeamEnum.White:
            return Knight.WhiteString
        elif team == Board.Constants.TeamEnum.Black:
            return Knight.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Knight

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        validMoves = []
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(2, 1), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(1, 2), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(-1, 2), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(-2, 1), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(-2, -1), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(-1, -2), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(1, -2), Knight.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(2, -1), Knight.MoveIterations, enforceKingUnderAttackCheck))
        return validMoves
