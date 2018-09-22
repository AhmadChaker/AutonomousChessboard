import Pieces.Constants
from Pieces.BasePiece import IBasePiece


class King(IBasePiece):

    def __init__(self, team):
        IBasePiece.__init__( self, team)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Pieces.Constants.TeamEnum.White:
            return u'\u2654'
        elif team == Pieces.Constants.TeamEnum.Black:
            return u'\u265A'

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.King
