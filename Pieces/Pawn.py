import Pieces.Constants
import Pieces.PieceHelpers
import Utilities.Points
import Utilities.Constants
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
        if team == Utilities.Constants.TeamEnum.White:
            return Pawn.WhiteString
        elif team == Utilities.Constants.TeamEnum.Black:
            return Pawn.BlackString

        return Utilities.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Pawn

    def GetValidMoves(self):
        isPieceMovingUpwards = (self.GetTeam() == Utilities.Constants.TeamEnum.White)
        moveIterNonKillMoves = 2 if len(self.GetHistory()) == 0 else 1
        moveIterToKillMoves = 1
        validMoves = []
        if isPieceMovingUpwards:
            logger.error("Getting Pawn non-kill moves")
            validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(0, 1), moveIterNonKillMoves))
            logger.error("Getting Pawn kill moves")
            validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-1, 1), moveIterToKillMoves))
            validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(1, 1), moveIterToKillMoves))
        else:
            logger.error("Getting Pawn non-kill moves")
            validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(0, -1), moveIterNonKillMoves))
            logger.error("Getting Pawn kill moves")
            validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-1, -1), moveIterToKillMoves))
            validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(1, -1), moveIterToKillMoves))
        return validMoves
