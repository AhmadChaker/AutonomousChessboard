import Pieces.Constants
import Pieces.PieceHelpers
import Utilities.Points
from Pieces.IBasePiece import IBasePiece


class Pawn(IBasePiece):

    WhiteString = u'\u2659'
    BlackString = u'\u265F'

    def __init__(self, team, coords):
        IBasePiece.__init__(self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Pieces.Constants.TeamEnum.White:
            return Pawn.WhiteString
        elif team == Pieces.Constants.TeamEnum.Black:
            return Pawn.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Pawn

    def GetValidMoves(self):
        isPieceMovingUpwards = (self.GetTeam() == Pieces.Constants.TeamEnum.White)
        moveIterations = 2 if len(self.GetHistory()) == 0 else 1

        validMoves = []
        if isPieceMovingUpwards:
            validMoves = Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(0, 1), moveIterations)
        else:
            validMoves = Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(0, -1), moveIterations)
        return validMoves
