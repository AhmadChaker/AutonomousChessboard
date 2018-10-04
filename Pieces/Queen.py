import sys
import Utilities.Points
import Utilities.Constants
import Pieces.Constants
from Pieces.IBasePiece import IBasePiece


class Queen(IBasePiece):

    WhiteString = u'\u2655'
    BlackString = u'\u265B'
    MoveIterations = sys.maxsize

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Utilities.Constants.TeamEnum.White:
            return Queen.WhiteString
        elif team == Utilities.Constants.TeamEnum.Black:
            return Queen.BlackString

        return Utilities.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Queen

    def GetValidMoves(self):
        validMoves = []
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(1, 1), Queen.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(1, 0), Queen.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(1, -1), Queen.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(0, -1), Queen.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-1, -1), Queen.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-1, 0), Queen.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-1, 1), Queen.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(0, 1), Queen.MoveIterations))
        return validMoves