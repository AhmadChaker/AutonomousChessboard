import logging
from multiprocessing import Process, Queue
import os
from guizero import App, Text, TextBox, PushButton
from Listeners.GameRequestListener import GameRequestListener
from Listeners.EngineRequestListener import EngineRequestListener
from Listeners.LogListener import LogListener
import Miscellaneous.Constants
from Listeners.Messages.EngineRequestMessages.EngineConfigurationMessage import EngineConfigurationMessage
from Listeners.Messages.GameRequestMessages.GameConfigurationMessage import GameConfigurationMessage
from Listeners.Messages.GameRequestMessages.GameMovementMessage import GameMovementMessage
from Listeners.Messages.Common.BaseMessage import BaseMessage, Actions
from Uci.Levels import LevelsList
from Utilities.OSConfiguration import OSConfiguration
from Miscellaneous.Constants import PlayerEnum


# region GUI element handlers

def StartClicked():

    # Game type  Human vs AI, AI vs AI, Human vs Human
    # In case of Human vs AI - Get color we want to start with

    # TODO: These properties will be configurable via user selection, hard-code these for testing right now
    gameType = Miscellaneous.Constants.GameType.AIvsAI
    humanColour = Miscellaneous.Constants.TeamEnum.White
    aiLevel = LevelsList[0]

    # Update the engine
    EngineRequestQueue.put(BaseMessage(Actions.Configuration, EngineConfigurationMessage(aiLevel)))

    # Kick off message processing
    GameRequestQueue.put(BaseMessage(Actions.Configuration, GameConfigurationMessage(gameType, humanColour)))


def ResetClicked():
    # TODO figure out how to purge queues
    EngineRequestQueue.put(BaseMessage(Actions.Reset, None))
    GameRequestQueue.put(BaseMessage(Actions.Reset, None))


def MoveClicked():
    # This is dummy input code. TODO: perform proper validation when audio inputter is working correctly
    moveCoords = MoveTextBox.value
    fromCoord = moveCoords[0] + moveCoords[1]
    toCoord = moveCoords[2] + moveCoords[3]
    GameRequestQueue.put(BaseMessage(Actions.Movement, GameMovementMessage(PlayerEnum.Human, fromCoord, toCoord)))
    MoveTextBox.clear()

# endregion


# Must run this first to setup multi-process logging
def StartLogProcess(logQueue):
    logListenerProcess = Process(target=LogListener.Listen, args=(logQueue,))
    logListenerProcess.daemon = True
    logListenerProcess.start()


# Every new process should call this method first to hookup multi-process logging
def ProcessStartupBaseTasks(logQueue):
    handler = logging.handlers.QueueHandler(logQueue)
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(logging.DEBUG)


def StartProcesses(logQueue, gameRequestListenerObj, engineRequestListenerObj):
    gameListenerProcess = Process(target=GameRequestListenerRunner, args=(logQueue, gameRequestListenerObj, ))
    gameListenerProcess.daemon = True
    gameListenerProcess.start()

    engineListenerProcess = Process(target=EngineRequestListenerRunner, args=(logQueue, engineRequestListenerObj))
    engineListenerProcess.daemon = True
    engineListenerProcess.start()


def GameRequestListenerRunner(logQueue, gameRequestListenerObj):
    ProcessStartupBaseTasks(logQueue)
    gameRequestListenerObj.StartListeningForRequests()


def EngineRequestListenerRunner(logQueue, engineRequestListenerObj):
    ProcessStartupBaseTasks(logQueue)
    engineRequestListenerObj.SetupEngine()
    engineRequestListenerObj.StartListeningForRequests()


def DrawGUI():
    # TODO: Implement actual proper test interaction interface instead of this dummy one
    app = App(title="ChessBoard", width=260, height=60, layout="grid")
    StartButton = PushButton(app, grid=[0, 0], text="Start", command=StartClicked)
    MoveTextBlock = Text(app, text="Move", grid=[1,0], align="left")
    MoveTextBox = TextBox(app, grid=[2, 0], align="left")
    GoButton = PushButton(app, grid=[3,0], text="Go", command=MoveClicked)
    ResetButton = PushButton(app, grid=[4, 0], text="Reset", command=ResetClicked)
    app.display()


if __name__ == '__main__':
    # Setup multi-process logging infrastructure
    LoggingQueue = Queue()
    StartLogProcess(LoggingQueue)

    # Setup logging for main process
    ProcessStartupBaseTasks(LoggingQueue)

    # Read from config file
    OSConfig = OSConfiguration()
    OSConfig.ReadConfiguration()
    # TODO handle case where EnginePath is not set due to not being able to read config file

    # Setup rest of variables
    GameRequestQueue = Queue()
    EngineRequestQueue = Queue()
    GameRequestListenerObj = GameRequestListener(GameRequestQueue, EngineRequestQueue)
    EngineRequestListenerObj = EngineRequestListener(OSConfig.PathToEngine, GameRequestQueue, EngineRequestQueue)

    # Run processes
    StartProcesses(LoggingQueue, GameRequestListenerObj, EngineRequestListenerObj)

    DrawGUI()
