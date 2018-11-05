import Pieces.Constants
import Miscellaneous.Points
import Board.Constants
from Utilities.BoardHelpers import BoardHelpers
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class Pawn(IBasePiece):

    WhiteString = u'\u2659'
    BlackString = u'\u265F'

    def __init__(self, team, coords):
        IBasePiece.__init__(self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Board.Constants.TeamEnum.White:
            return Pawn.WhiteString
        elif team == Board.Constants.TeamEnum.Black:
            return Pawn.BlackString

        return Board.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Pawn

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        isPieceMovingUpwards = (self.GetTeam() == Board.Constants.TeamEnum.White)
        moveIterNonKillMoves = 2 if len(self.GetHistory()) == 1 else 1
        moveIterToKillMoves = 1
        validMoves = []
        if isPieceMovingUpwards:
            validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(0, 1), moveIterNonKillMoves, enforceKingUnderAttackCheck))
            validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(-1, 1), moveIterToKillMoves, enforceKingUnderAttackCheck))
            validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(1, 1), moveIterToKillMoves, enforceKingUnderAttackCheck))
        else:
            validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(0, -1), moveIterNonKillMoves, enforceKingUnderAttackCheck))
            validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(-1, -1), moveIterToKillMoves, enforceKingUnderAttackCheck))
            validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(1, -1), moveIterToKillMoves, enforceKingUnderAttackCheck))
        return validMoves
