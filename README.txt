A python implementation of the game "Rush Hour" where the goal is to get the red car to the exit by moving around the other cars.
This program uses the "pygame" module to deal with game effects and graphics.

The text-only version of the game is called 'rushhour.py'.
The gui game is called 'rushhourGui.py' and imports some of the classes from the text based game.
A sample game ('game2.txt') is included in what I submitted but any of the example game files will work.

Note on text game:
	After selecting a car (choosing the letter), the cars will move by being given an integer.
The cars will move horizontally of vertically based on the game file.
If the int given is positive the car will move (right / down) and if it is negative the car will move (left / up) all based on their orientation.
The target car will always be named 'A'.

Note on gui game:
	The cars move by first clicking on a car and then to a spot you want to move the car.
The car will remember the position you picked and move that part of the car to wherever you choose.
That is to say, if you clock on the middle of the car and then on another tile, that is where the middle of the car will end up (if it is a valid move).
The red car will always be the target.
The game will close roughly 1.5 seconds after a player wins.
