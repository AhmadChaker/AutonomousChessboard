import sys
import Pieces.Constants
import Miscellaneous.Points
import Board.Constants
from Utilities.BoardHelpers import BoardHelpers
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class Bishop(IBasePiece):

    WhiteString = u'\u2657'
    BlackString = u'\u265D'
    MoveIterations = sys.maxsize

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Board.Constants.TeamEnum.White:
            return Bishop.WhiteString
        elif team == Board.Constants.TeamEnum.Black:
            return Bishop.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Bishop

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        validMoves = []
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(1, 1), Bishop.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(1, -1), Bishop.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(-1, 1), Bishop.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(-1, -1), Bishop.MoveIterations, enforceKingUnderAttackCheck))
        return validMoves
