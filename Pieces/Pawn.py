import Pieces.Constants
import Board.Constants
from Miscellaneous.Points import Points
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
        # In case pawns are starting from a non standard position, need additional processing
        moveIterNonKillMoves = 1
        if (isPieceMovingUpwards and self.GetCoordinates().GetY() == Board.Constants.WHITE_PAWNS_Y_ARRAY_COORDINATE) or \
                ((not isPieceMovingUpwards) and self.GetCoordinates().GetY() == Board.Constants.BLACK_PAWNS_Y_ARRAY_COORDINATE):
            moveIterNonKillMoves = 2

        moveIterToKillMoves = 1
        validMoves = []
        if isPieceMovingUpwards:
            validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(0, 1), moveIterNonKillMoves, enforceKingUnderAttackCheck))
            validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(-1, 1), moveIterToKillMoves, enforceKingUnderAttackCheck))
            validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(1, 1), moveIterToKillMoves, enforceKingUnderAttackCheck))
        else:
            validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(0, -1), moveIterNonKillMoves, enforceKingUnderAttackCheck))
            validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(-1, -1), moveIterToKillMoves, enforceKingUnderAttackCheck))
            validMoves.extend(BoardHelpers.GetValidMoves(self, board, Points(1, -1), moveIterToKillMoves, enforceKingUnderAttackCheck))
        return validMoves
