import Pieces.Constants
import Utilities.Points
import Board.Constants
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class King(IBasePiece):

    WhiteString = u'\u2654'
    BlackString = u'\u265A'

    MoveIterations = 1

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Board.Constants.TeamEnum.White:
            return King.WhiteString
        elif team == Board.Constants.TeamEnum.Black:
            return King.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.King

    def GetValidMoves(self, board):
        validMoves = []
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(1, 1), King.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(1, 0), King.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(1, -1), King.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(0, -1), King.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(-1, -1), King.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(-1, 0), King.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(-1, 1), King.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, board, Utilities.Points.Points(0, 1), King.MoveIterations))
        return validMoves
