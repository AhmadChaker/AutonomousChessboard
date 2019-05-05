import logging
import os
import Utilities.GameHelpers
from Game.Game import Game
from Board.ChessBoard import ChessBoard
from Board.History import History
from Listeners.Messages.Common.BaseMessage import Actions, BaseMessage
from Listeners.Messages.GameRequestMessages.GameMovementMessage import GameMovementMessage
from Listeners.Messages.GameRequestMessages.GameConfigurationMessage import GameConfigurationMessage
from Listeners.Messages.EngineRequestMessages.EngineMoveMessage import EngineMoveMessage
from Miscellaneous.Constants import GameType, PlayerEnum, TeamEnum


logger = logging.getLogger(__name__)


class GameRequestListener:

    def __init__(self, gameRequestQueue, engineRequestQueue):
        self.__game = Game(ChessBoard(History()))
        self.__gameRequestQueue = gameRequestQueue
        self.__engineRequestQueue = engineRequestQueue
        self.__gameType = None
        self.__humanPlayerColor = None

    def UpdateGameOptions(self, gameType, humanPlayerColor):
        logger.error("About to update game options")
        self.__gameType = gameType
        self.__humanPlayerColor = humanPlayerColor
        logger.error("Updated game options")

    def StartGame(self):
        logger.error("Setting up game of GameType: " + str(self.__gameType))

        gameType = self.__gameType
        if not Utilities.GameHelpers.GameHelpers.IsValidGameType(gameType):
            logger.error("Unhandled game type: " + str(self.__gameType))
            # TODO notify user to enter a valid game type
            return

        if self.__gameType == GameType.AIvsHuman:
            if self.__humanPlayerColor == TeamEnum.Black:
                # Add to AI queue
                self.SendMoveRequestToEngine(self.__game.GetFenRepresentation())

        elif self.__gameType == GameType.AIvsAI:
            self.SendMoveRequestToEngine(self.__game.GetFenRepresentation())
        elif self.__gameType == GameType.HumanvsHuman:
            # Wait for human input
            pass

        logging.error("Exiting setup")

    def StartListeningForRequests(self):
        logger.error("Started listening for requests, PID: " + str(os.getpid()))

        while True:
            logger.error("Waiting to pop item off queue")
            poppedItem = self.__gameRequestQueue.get()
            logger.error("Item popped")
            if poppedItem.Action == Actions.Movement:
                self.ProcessMove(poppedItem.Object)
            elif poppedItem.Action == Actions.Configuration:
                self.ProcessConfigurationChange(poppedItem.Object)
            elif poppedItem.Action == Actions.Reset:
                self.ResetState()
            else:
                logger.error("popped item is of unknown type")
                continue

    def ResetState(self):
        logging.info("About to purge game queue")
        while not self.__gameRequestQueue.empty():
            self.__gameRequestQueue.get()
        logging.info("Purged game queue successfully")
        self.__game.ResetGame()

    def ProcessConfigurationChange(self, configMessage:GameConfigurationMessage):
        self.UpdateGameOptions(configMessage.GameType, configMessage.ColorOfHumanPlayer)
        self.StartGame()

    def ProcessMove(self, moveMessage:GameMovementMessage):
        # need to see if it's this persons move!
        moveResult = self.__game.Move(moveMessage.MoveFrom, moveMessage.MoveTo)
        personWhoIsMoving = moveMessage.Person
        if not moveResult.IsSuccessful():
            if not Utilities.GameHelpers.GameHelpers.IsValidPlayerEnum(personWhoIsMoving):
                logger.error("Unknown person quantity: " + str(personWhoIsMoving))

            if personWhoIsMoving == PlayerEnum.Human:
                logger.error("Unsuccessful move by human player")
            elif personWhoIsMoving == PlayerEnum.AI:
                logger.error("Invalid move by AI, this should only happen due to timing effects when reset is hit")
            return

        # Post move processing
        # TODO send these out to the UI queue
        if self.__game.GetIsInCheckmate():
            logger.error("Game is in checkmate!")
            return

        if self.__game.GetIsDraw():
            logger.error("Game has ended in a draw!")
            return

        if self.__game.GetIsInCheck():
            logger.error("Player is in check!")

        # Setup the relevant move response (if applicable)
        gameType = self.__gameType
        if not Utilities.GameHelpers.GameHelpers.IsValidGameType(gameType):
            logger.error("Unhandled game type: " + str(self.__gameType))
            return

        if self.__gameType == GameType.AIvsHuman:
            if personWhoIsMoving == PlayerEnum.Human:
                # Add to AI queue
                self.SendMoveRequestToEngine(self.__game.GetFenRepresentation())
        elif self.__gameType == GameType.AIvsAI:
            self.SendMoveRequestToEngine(self.__game.GetFenRepresentation())
        elif self.__gameType == GameType.HumanvsHuman:
            # Wait for human input
            pass

    def SendMoveRequestToEngine(self, fenRep):
        self.__engineRequestQueue.put(BaseMessage(Actions.Movement, EngineMoveMessage(fenRep)))

