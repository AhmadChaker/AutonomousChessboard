import Pieces.Constants
from Pieces.IBasePiece import IBasePiece


class Queen(IBasePiece):

    WhiteString = u'\u2655'
    BlackString = u'\u265B'

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Pieces.Constants.TeamEnum.White:
            return Queen.WhiteString
        elif team == Pieces.Constants.TeamEnum.Black:
            return Queen.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Queen

    def CanMove(self):
        return True

    def Move(self):
        return True

    def GetValidMoves(self):
        return True