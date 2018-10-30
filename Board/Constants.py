from enum import Enum

# Valid chess board coordinates
ALPHABETICAL_BOARD_ORDINATES = "ABCDEFGH"
NUMERICAL_BOARD_ORDINATES = "12345678"

# Board dimensions
MAXIMUM_X_SQUARES = 8
MAXIMUM_Y_SQUARES = 8

# Gameplay constants
DRAW_CONDITION_TOTAL_MOVES = 150

# Castling related constants
KING_CASTLE_SQUARE_MOVES = 2
BISHOP_CASTLE_LEFT_TO_RIGHT_MOVES = 3
BISHOP_CASTLE_RIGHT_TO_LEFT_MOVES = 2


class TeamEnum(Enum):
    NoTeam = 1
    White = 2
    Black = 3


