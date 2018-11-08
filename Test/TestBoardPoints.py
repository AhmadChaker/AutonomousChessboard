import unittest
import Miscellaneous.BoardPoints
from Miscellaneous.BoardPoints import BoardPoints


class TestPoints(unittest.TestCase):

    def test_Init_XArrayOutOfRange_ReturnsBadValues(self):
        boardPoint = BoardPoints(-5,5)

        self.assertEqual(boardPoint, Miscellaneous.BoardPoints.BOARD_POINTS_UNDEFINED)

    def test_Init_YArrayOutOfRange_ReturnsBadValues(self):
        boardPoint = BoardPoints(5, -5)

        self.assertEqual(boardPoint, Miscellaneous.BoardPoints.BOARD_POINTS_UNDEFINED)

    def test_Init_XYInRange_ReturnsValid(self):
        boardPoint = BoardPoints(3, 6)

        expectedXBoardCoordinate = "D"
        expectedYBoardCoordinate = "7"

        self.assertEqual(boardPoint.GetXBoard(), expectedXBoardCoordinate)
        self.assertEqual(boardPoint.GetYBoard(), expectedYBoardCoordinate)

    def test_LessThan_XDifferent(self):
        boardPointA = BoardPoints(3,6)
        boardPointB = BoardPoints(4,6)
        self.assertLess(boardPointA, boardPointB)

    def test_LessThan_XSameYDifferent(self):
        boardPointA = BoardPoints(3,5)
        boardPointB = BoardPoints(3,6)
        self.assertLess(boardPointA, boardPointB)

