# Autonomous Chess
## Aim
The aim of this project is to develop an autonomous chessboard that accepts voice commands to move physical chess pieces autonomously (i.e. without any human involvement).

The board shall operate in three modes:
1) 1 Human vs 1 AI
2) 1 Human vs 1 Human 
3) 1 AI vs 1 AI

## Minimum viable product
The minimum viable product must fulfil the following criteria:
- 	Allow a human player to either use their hand or issue audio commands to move pieces.
- 	Board must handle misregistered moves
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

## Language choice
Python is used as the language of choice in this project for the following reasons:
1) Extensive and well supported python libraries for interacting with all Raspberry Pi peripherals (sensors, logic boards etc)
2) A desire to learn a different style of programming language

## Installation guide
TODO: More details on installation on various packages
### Windows 
pip install guizero

### Linux

sudo pip3 install guizero

## Major to do items remaining
- Choice of offline audio processing library
- Purchase and test hall effect sensors for piece detection
- Hook into the 2 degree of freedom "robot table" obtained.

## Further information
For further information consult the Documentation folder.

