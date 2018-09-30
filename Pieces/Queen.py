import Pieces.Constants
from Pieces.IBasePiece import IBasePiece


class Queen(IBasePiece):

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Pieces.Constants.TeamEnum.White:
            return u'\u2655'
        elif team == Pieces.Constants.TeamEnum.Black:
            return u'\u265B'

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Queen

    def CanMove(self, chessBoard):
        return True

    def Move(self, chessBoard):
        return True
