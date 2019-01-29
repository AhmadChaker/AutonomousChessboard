import logging
import os
import Miscellaneous.Constants
from Miscellaneous.Constants import PlayerEnum
from Listeners.Messages.EngineRequestMessages.EngineConfigurationMessage import EngineConfigurationMessage
from Listeners.Messages.EngineRequestMessages.EngineMoveMessage import EngineMoveMessage
from Listeners.Messages.GameRequestMessages.GameMovementMessage import GameMovementMessage
from Listeners.Messages.Common.BaseMessage import BaseMessage, Actions
from Uci.Engine import Engine


logger = logging.getLogger(__name__)


class EngineRequestListener:

    def __init__(self, pathToEngine, gameRequestQueue, engineRequestQueue):
        self.__pathToEngine = pathToEngine
        self.GameRequestQueue = gameRequestQueue
        self.EngineRequestQueue = engineRequestQueue
        self.Engine = None
        self.Level = None
        self.__hasSetupBeenRun = False

    def UpdateOptions(self, engineConfigMessage:EngineConfigurationMessage):
        logger.error("About to update options")
        self.Level = engineConfigMessage.Level
        self.Engine.ConfigureLevel(self.Level)
        logger.error("Updated options")

    def SetupEngine(self):
        logger.error("Setting up engine")

        self.Engine = Engine(self.__pathToEngine)
        hasStarted = self.Engine.StartEngine()

        self.__hasSetupBeenRun = True
        logging.error("Exiting setup, IsStarted: " + str(hasStarted))
        return hasStarted

    def StartListeningForRequests(self):
        logger.error("PID: " + str(os.getpid()))

        while True:
            logger.error("Waiting to pop item off queue")
            poppedItem = self.EngineRequestQueue.get()
            logger.error("Item popped")

            if not self.__hasSetupBeenRun:
                logger.error("Setup was not run, running it now")
                self.Setup()

            if poppedItem.Action == Actions.Configuration:
                self.UpdateOptions(poppedItem.Object)
            elif poppedItem.Action == Actions.Movement:
                obtainedMove = self.GetMoveFromEngine(poppedItem.Object)
                # TODO handle case where obtainedMove is Null, how do we propagate this back to the UI thread?
                if obtainedMove is not None:
                    self.PropagateObtainedMove(obtainedMove)
            elif poppedItem.Action == Actions.Reset:
                logging.info("Test for purging")
                self.ResetState()
            else:
                logger.error("popped item is of unknown type")
                continue

            logger.error("Finished processing")

    def ResetState(self):
        logging.info("About to purge engine queue")
        while not self.EngineRequestQueue.empty():
            self.EngineRequestQueue.get()
        logging.info("Purged engine queue successfully")

    def GetMoveFromEngine(self, engineMoveObj:EngineMoveMessage):
        if not self.Engine.IsAlive():
            logger.error("Engine is dead, spwan a new engine")
            hasStarted = self.Setup()
            logger.error("Tried to startup engine, HasStarted: " + str(hasStarted))
            if not hasStarted:
                # TODO how to handle this ? Keep trying to start the engine on loop every 10 seconds for about a minute
                pass
        moveObj = self.Engine.ObtainMove(engineMoveObj.FenRepresentation)
        if moveObj is None or moveObj.bestmove is None:
            return None
        return moveObj.bestmove.uci()

    def PropagateObtainedMove(self, bestMove):
        strBestMove = str(bestMove)
        logger.error("Best Move: " + strBestMove)
        # In pawn promotion UCI looks like c2c1q where q is the piece to replace it with, we assume its always queen
        # For Castling, it is signified by the King moving two spots so it's a standard move
        if len(strBestMove) != 2* Miscellaneous.Constants.STRING_CHARACTERS_IN_COORDINATE and \
                len(strBestMove) != (2 * Miscellaneous.Constants.STRING_CHARACTERS_IN_COORDINATE + 1) :
            logger.error("Length of BestMove (" + str(len(strBestMove)) + ") is unexpected")
            return

        fromCoord = bestMove[0] + bestMove[1]
        toCoord = bestMove[2] + bestMove[3]

        self.GameRequestQueue.put(BaseMessage(Actions.Movement,
                                              GameMovementMessage(PlayerEnum.AI, fromCoord, toCoord)))
