import sys
import Utilities.Points
import Utilities.Constants
import Pieces.Constants
import Pieces.PieceHelpers
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class Rook(IBasePiece):

    WhiteString = u'\u2656'
    BlackString = u'\u265C'
    MoveIterations = sys.maxsize

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Utilities.Constants.TeamEnum.White:
            return Rook.WhiteString
        elif team == Utilities.Constants.TeamEnum.Black:
            return Rook.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Rook

    def GetValidMoves(self, board):
        validMoves = []
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(1, 0), Rook.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(0, 1), Rook.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(-1, 0), Rook.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(0, -1), Rook.MoveIterations))
        return validMoves
