import Pieces.Constants
from Pieces.IBasePiece import IBasePiece


class Knight(IBasePiece):

    WhiteString = u'\u2658'
    BlackString = u'\u265E'

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

    def CanMove(self):
        return True

    def Move(self):
        return True

    def GetValidMoves(self):
        return True