import Chessboard
import Pieces.Constants
from Pieces.IBasePiece import IBasePiece


class Bishop(IBasePiece):

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Pieces.Constants.TeamEnum.White:
            return u'\u2657'
        elif team == Pieces.Constants.TeamEnum.Black:
            return u'\u265D'

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Bishop

    def CanMove(self, piece:IBasePiece, chessBoard: Chessboard) -> bool:
        return True

    def Move(self, chessBoard: Chessboard) -> bool:
        return True
