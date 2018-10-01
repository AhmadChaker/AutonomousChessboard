import Pieces.Constants
from Pieces.IBasePiece import IBasePiece


class Rook(IBasePiece):

    WhiteString = u'\u2656'
    BlackString = u'\u265C'

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Pieces.Constants.TeamEnum.White:
            return Rook.WhiteString
        elif team == Pieces.Constants.TeamEnum.Black:
            return Rook.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Rook

    def CanMove(self, chessBoard):
        return True

    def Move(self, chessBoard):
        return True

    def GetValidMoves(self, chessBoard):
        return True