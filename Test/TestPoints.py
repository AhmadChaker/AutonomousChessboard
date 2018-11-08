import unittest
import Board.Constants
from Miscellaneous.BoardPoints import Points


class TestPoints(unittest.TestCase):

    def test_Init_XArrayOutOfRange_ReturnsBadValue(self):
        arrCoords = Points(-5,-10)



        self.assertEqual(move2, move1)