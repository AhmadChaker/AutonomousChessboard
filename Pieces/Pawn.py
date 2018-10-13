import Pieces.Constants
import Pieces.PieceHelpers
import Utilities.Points
import Board.Constants
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

    def GetValidMoves(self, board):
        isPieceMovingUpwards = (self.GetTeam() == Board.Constants.TeamEnum.White)
        moveIterNonKillMoves = 2 if len(self.GetHistory()) == 0 else 1
        moveIterToKillMoves = 1
        validMoves = []
        if isPieceMovingUpwards:
            validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(0, 1), moveIterNonKillMoves))
            validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(-1, 1), moveIterToKillMoves))
            validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(1, 1), moveIterToKillMoves))
        else:
            validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(0, -1), moveIterNonKillMoves))
            validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(-1, -1), moveIterToKillMoves))
            validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(1, -1), moveIterToKillMoves))
        return validMoves
