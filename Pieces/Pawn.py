import Pieces.Constants
import Pieces.PieceHelpers
import Utilities.Points
from Pieces.IBasePiece import IBasePiece


class Pawn(IBasePiece):

    WhiteString = u'\u2659'
    BlackString = u'\u265F'

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Pieces.Constants.TeamEnum.White:
            return Pawn.WhiteString
        elif team == Pieces.Constants.TeamEnum.Black:
            return Pawn.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Pawn

    def CanMove(self, toMovePoint:Utilities.Points.Points):

        if toMovePoint == Utilities.Points.POINTS_UNDEFINED:
            return False

        validMoves = self.GetValidMoves()
        if len(validMoves) == 0:
            return False

        if any(obj['shape'] == 'square' for obj in shapes):

        return True

    def Move(self):

        if not self.CanMove(self):
            return False

        return True

    def GetValidMoves(self):

        isPieceMovingUpwards = (self.GetTeam() == Pieces.Constants.TeamEnum.White)
        moveIterations = 2 if len(self.GetHistory()) == 0 else 1

        validMoves = []
        if isPieceMovingUpwards:
            validMoves = Pieces.PieceHelpers.GetValidMoves(self, Points(0, 1), moveIterations)
        else:
            validMoves = Pieces.PieceHelpers.GetValidMoves(self, Points(0, -1), moveIterations)

        return validMoves

    def GetValidMoves(self, chessBoard):
        return True