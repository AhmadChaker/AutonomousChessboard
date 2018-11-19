class MoveEnum:
    Success = 1
    CoordOutOfRange = 2
    SlotHasNoTeam = 3
    WrongTeam = 4
    InvalidPieceCentricMove = 5
    GameEnded = 6


MoveMessageDictionary = {
    MoveEnum.Success: "Successful",
    MoveEnum.CoordOutOfRange: "Invalid move, coordinate is out of range",
    MoveEnum.SlotHasNoTeam: "Invalid move, no piece at coordinate",
    MoveEnum.WrongTeam: "Invalid move, not this teams turn",
    MoveEnum.InvalidPieceCentricMove: "Invalid move, piece can't move to this location",
    MoveEnum.GameEnded: "Game has already ended, start a new game"
}
