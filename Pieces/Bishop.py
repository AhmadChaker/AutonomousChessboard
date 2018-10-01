import Chessboard
import Pieces.Constants
from Pieces.IBasePiece import IBasePiece


class Bishop(IBasePiece):

    WhiteString = u'\u2657'
    BlackString = u'\u265D'

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

    def CanMove(self) -> bool:
        return True

    def Move(self) -> bool:
        return True

    def GetValidMoves(self):
        return True

