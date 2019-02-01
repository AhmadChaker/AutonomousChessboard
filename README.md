# Autonomous Chess
## Aim
The aim of this project is to develop an autonomous chessboard that accepts voice commands to move physical chess pieces autonomously (i.e. without any human involvement).

The board will play in three modes:
1) 1 Human vs 1 AI
2) 1 Human vs 1 Human 
3) 1 AI vs 1 AI (Demonstration purposes)

## Why work on this project?
The primary driver for this project is a desire to allow disabled persons to enjoy the games they love at a low cost.
The usage of a Raspberry Pi along with open-source components facilitates the development of a low-cost solution.

## Minimum viable product
The minimum viable product must fulfil the following criteria:
- 	Allow a human player to either use their hand or issue audio commands to move pieces.
- 	Pieces must navigate the board without touching each other.
-	The board must permit the selection of 15 difficulty levels.
-	Recognise check, checkmate and draw conditions and notify the user
-	Startable via audio commands
-	Have a single electrical plug that will be rechargeable and supply 12V to the motor system and 5V to the raspberry pi.

## Chess engine 
The chess engine being used is StockFish. The choice of engine is due to the following characteristics:
-	Open source	
-	Numerous libraries available
-	Cross-platform
-	Easily configurable


## Installation guide
TODO: More details on installation on various packages
### Windows 
pip install guizero

### Linux

sudo pip3 install guizero

## Further information
For further information please consult the Documentation folder.