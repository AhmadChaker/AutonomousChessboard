import sys
import Chessboard
import Pieces.Constants
import Utilities.Points
from Pieces.IBasePiece import IBasePiece


class Bishop(IBasePiece):

    WhiteString = u'\u2657'
    BlackString = u'\u265D'
    MoveIterations = sys.maxsize

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Pieces.Constants.TeamEnum.White:
            return Bishop.WhiteString
        elif team == Pieces.Constants.TeamEnum.Black:
            return Bishop.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Bishop

    def GetValidMoves(self):
        validMoves = []
        validMoves.extend(Pieces.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(1, 1), Bishop.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(1, -1), Bishop.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-1, 1), Bishop.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-1, -1), Bishop.MoveIterations))
        return validMoves


