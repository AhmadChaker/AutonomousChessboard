import sys
import Utilities.Points
import Board.Constants
import Pieces.Constants
from Utilities.BoardHelpers import BoardHelpers
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class Queen(IBasePiece):

    WhiteString = u'\u2655'
    BlackString = u'\u265B'
    MoveIterations = sys.maxsize

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Board.Constants.TeamEnum.White:
            return Queen.WhiteString
        elif team == Board.Constants.TeamEnum.Black:
            return Queen.BlackString

        return Board.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Queen

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        validMoves = []
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Utilities.Points.Points(1, 1), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Utilities.Points.Points(1, 0), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Utilities.Points.Points(1, -1), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Utilities.Points.Points(0, -1), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Utilities.Points.Points(-1, -1), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Utilities.Points.Points(-1, 0), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Utilities.Points.Points(-1, 1), Queen.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Utilities.Points.Points(0, 1), Queen.MoveIterations, enforceKingUnderAttackCheck))
        return validMoves
