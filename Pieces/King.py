import Pieces.Constants
from Pieces.IBasePiece import IBasePiece


class King(IBasePiece):

    WhiteString = u'\u2654'
    BlackString = u'\u265A'

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Pieces.Constants.TeamEnum.White:
            return King.WhiteString
        elif team == Pieces.Constants.TeamEnum.Black:
            return King.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.King

    def CanMove(self):
        return True

    def Move(self):
        return True

    def GetValidMoves(self):
        return True
