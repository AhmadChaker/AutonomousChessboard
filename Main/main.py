import logging
from Main import Game
from Miscellaneous.Messages import Status
from Utilities.MoveHelpers import MoveHelpers
from guizero import App, Text, TextBox, PushButton, info

# setup logger
logging.basicConfig(handlers=[logging.FileHandler('..\log.txt', 'w', 'utf-8')],
                    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(name)s %(funcName)s %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.DEBUG)

t1 = Game.Game()
MoveHelpers.Update(t1.GetHistory())

t1.PrintProperties()


def ClickedButton():
    fromBoardCoordValue = FromCoordinateTextBox.value
    toBoardCoordValue = ToCoordinateTextBox.value

    canMoveResult = t1.CanMove(fromBoardCoordValue, toBoardCoordValue)
    if canMoveResult.GetStatus() == Status.Report:
        info("Alert", canMoveResult.GetMessage())
        return

    moveResult = t1.Move(fromBoardCoordValue, toBoardCoordValue)
    if moveResult.GetStatus() == Status.Report:
        info("Alert", moveResult.GetMessage())
        return


app = App(title="Sheena", width=600, height=600, layout="grid")
FromCoordinateTextBlock = Text(app, text="From Coordinates", grid=[0,0], align="left")
FromCoordinateTextBox = TextBox(app, grid=[1,0], align="left")
ToCoordinateTextBlock = Text(app, text="To Coordinates", grid=[2,0], align="left")
ToCoordinateTextBox = TextBox(app, grid=[3,0], align="left")
GoButton = PushButton(app, grid=[4,0], text="Go", command=ClickedButton)
app.display()

