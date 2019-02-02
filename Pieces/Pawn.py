import Miscellaneous.Constants
from Miscellaneous.Constants import TeamEnum, PieceEnums
from Miscellaneous.Points import Points
from Utilities.MoveHelpers import MoveHelpers
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class Pawn(IBasePiece):

    WhitePieceString = u'\u2659'
    BlackPieceString = u'\u265F'
    WhitePieceFenString = 'P'
    BlackPieceFenString = 'p'

    def __init__(self, team, coords):
        IBasePiece.__init__(self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == TeamEnum.White:
            return Pawn.WhitePieceString
        elif team == TeamEnum.Black:
            return Pawn.BlackPieceString

        return Miscellaneous.Constants.BOARD_ERROR_STRING

    def GetFenRepresentation(self):
        team = self.GetTeam()
        if team == TeamEnum.White:
            return Pawn.WhitePieceFenString
        elif team == TeamEnum.Black:
            return Pawn.BlackPieceFenString

        return Miscellaneous.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Miscellaneous.Constants.PieceEnums.Pawn

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        isPieceMovingUpwards = (self.GetTeam() == TeamEnum.White)
        # In case pawns are starting from a non standard position, need additional processing
        moveIterNonKillMoves = 1
        if (isPieceMovingUpwards and self.GetCoordinates().GetY() == Miscellaneous.Constants.WHITE_PAWNS_Y_ARRAY_COORDINATE) or \
                ((not isPieceMovingUpwards) and self.GetCoordinates().GetY() == Miscellaneous.Constants.BLACK_PAWNS_Y_ARRAY_COORDINATE):
            moveIterNonKillMoves = 2

        moveIterToKillMoves = 1
        validMoves = []
        if isPieceMovingUpwards:
            validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(0, 1), moveIterNonKillMoves, enforceKingUnderAttackCheck))
            validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-1, 1), moveIterToKillMoves, enforceKingUnderAttackCheck))
            validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(1, 1), moveIterToKillMoves, enforceKingUnderAttackCheck))
        else:
            validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(0, -1), moveIterNonKillMoves, enforceKingUnderAttackCheck))
            validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-1, -1), moveIterToKillMoves, enforceKingUnderAttackCheck))
            validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(1, -1), moveIterToKillMoves, enforceKingUnderAttackCheck))
        return validMoves
