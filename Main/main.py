import logging
from Main.Game import Game
from Board.ChessBoard import ChessBoard
from Board.History import History
from Utilities.MoveHelpers import MoveHelpers
from guizero import App, Text, TextBox, PushButton, info

# setup logger
logging.basicConfig(handlers=[logging.FileHandler('..\log.txt', 'w', 'utf-8')],
                    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(name)s %(funcName)s %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.DEBUG)

history = History()
chessBoard = ChessBoard()
t1 = Game(history, chessBoard)
MoveHelpers.Update(history)

t1.PrintProperties()


def ClickedButton():
    fromBoardCoordValue = FromCoordinateTextBox.value
    toBoardCoordValue = ToCoordinateTextBox.value

    canMoveResult = t1.CanMove(fromBoardCoordValue, toBoardCoordValue)
    if not canMoveResult.IsSuccessful():
        info("Alert", canMoveResult.GetMessage())
        return

    moveResult = t1.Move(fromBoardCoordValue, toBoardCoordValue)
    if not moveResult.IsSuccessful():
        info("Alert", moveResult.GetMessage())
        return

    if t1.GetIsInCheckmate():
        info("Alert", "Checkmate!")
        return

    if t1.GetIsDraw():
        info("Alert", "Draw!")
        return

    if t1.GetIsInCheck():
        info("Alert", "Check!")
        return


app = App(title="Sheena", width=600, height=600, layout="grid")
FromCoordinateTextBlock = Text(app, text="From Coordinates", grid=[0,0], align="left")
FromCoordinateTextBox = TextBox(app, grid=[1,0], align="left")
ToCoordinateTextBlock = Text(app, text="To Coordinates", grid=[2,0], align="left")
ToCoordinateTextBox = TextBox(app, grid=[3,0], align="left")
GoButton = PushButton(app, grid=[4,0], text="Go", command=ClickedButton)
app.display()

