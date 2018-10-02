import Utilities.Points
import Pieces.Constants
from Pieces.IBasePiece import IBasePiece


class Knight(IBasePiece):

    WhiteString = u'\u2658'
    BlackString = u'\u265E'
    MoveIterations = 1

    def __init__(self, team, coords):
        IBasePiece.__init__(self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Pieces.Constants.TeamEnum.White:
            return Knight.WhiteString
        elif team == Pieces.Constants.TeamEnum.Black:
            return Knight.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Knight

    def GetValidMoves(self):
        validMoves = []
        validMoves.extend(Pieces.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(2, 1), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(1, 2), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-1, 2), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-2, 1), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-2, -1), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-1, -2), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(1, -2), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(2, -1), Knight.MoveIterations))
        return validMoves
