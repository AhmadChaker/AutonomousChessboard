from enum import Enum

# Valid chess board coordinates
ALPHABETICAL_BOARD_ORDINATES = "ABCDEFGH"
NUMERICAL_BOARD_ORDINATES = "12345678"

MAXIMUM_X_SQUARES = 8
MAXIMUM_Y_SQUARES = 8


class TeamEnum(Enum):
    NoTeam = 1
    White = 2
    Black = 3


