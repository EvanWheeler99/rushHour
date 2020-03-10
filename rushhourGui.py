import sys
import string
import pygame
import time

from rushhour import Game
from rushhour import Car
from rushhour import Board



class Gui:
	'''
	All of the methods needed to run the gui game are in this class.
	To run the game with a gui, the class uses an instance of the Game class from the text based game.
	The class has a mainloop method that runs a game when called.
	'''
	def __init__(self, game):
		'''
		This initializes the gui by calling an instance of game
		The variables correspond to the dimensions of the board
		'''
		self.game = game
		self.game.board.car_spawn()
		self.matrix = self.game.board.matrix
		self.gridSize = self.game.gridSize
		self.grid_block_size = 75
		self.lines = 5
		self.screenBorderSize = self.grid_block_size
		self.width = ((self.grid_block_size + self.lines)
 					* (self.game.board.gridSize))
		self.height = self.width
		pygame.init()
		self.window = pygame.display.set_mode((self.width + (self.screenBorderSize * 2), self.height + (self.screenBorderSize * 2)))
		pygame.font.init()
		self.font = pygame.font.SysFont('Helvetica', 60)


	def mainloop(self):
		'''
		The main game method.
		After creating the board, the method loops continuously untill the game is closed or won.
		After winning the game, 'You Win!' will be displayed on screen and then the program will close after a delay.
		'''
		textColour = (0,255,0)
		self.keepLooping = True
		while self.keepLooping:

			self.draw_board()

			for ev in pygame.event.get():
				if (ev.type == pygame.QUIT):
					self.keepLooping = False

				if (self.game.is_game_over() == True):
					self.draw_board()
					text = self.font.render('You Win!',False,textColour)
					self.window.blit(text,(self.width / 2 ,0))
					pygame.display.update()
					time.sleep(1.5)
					self.keepLooping = False

				if (ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1):
					self.mouse_down(ev.pos)
			#The game is now over


	def draw_board(self):
		'''
		This section draws everything you see on screen.
		First it makes the board, then is places all of the cars in the 'garage' onto the Board
		It makes use of the draw_car method to help split up the code
		After everything is drawn it updates the display.
		'''
		textColour = (0,255,0)
		borderColour = (50, 50, 50)#dark grey
		bGColour = (100, 100, 100)# Grey
		lineColour = (0,0,0)
		#Fill the entire window
		self.window.fill(borderColour)

		#Making the grid surface
		pygame.draw.rect(self.window, bGColour, [(self.screenBorderSize),(self.screenBorderSize),self.height,self.width])

		#Drawing the exit
		pygame.draw.rect(self.window, bGColour, [self.width + self.screenBorderSize, self.screenBorderSize + self.lines/2 + (self.grid_block_size + self.lines)*2,self.screenBorderSize,self.screenBorderSize])

		pygame.draw.line(self.window, lineColour, (self.width + self.screenBorderSize,self.screenBorderSize + (self.grid_block_size+self.lines)*2),(self.width + self.screenBorderSize + self.screenBorderSize,self.screenBorderSize + (self.grid_block_size+self.lines)*2), self.lines)

		pygame.draw.line(self.window, lineColour, (self.width + self.screenBorderSize,self.screenBorderSize + (self.grid_block_size+self.lines)*3),(self.width + self.screenBorderSize + self.screenBorderSize,self.screenBorderSize + (self.grid_block_size+self.lines)*3), self.lines)

		#Draw vertical gridlines
		for i in range(self.gridSize +1):
			pygame.draw.line(self.window, lineColour, ((i)*self.grid_block_size + (i)*self.lines + self.screenBorderSize, self.screenBorderSize),
				((i)*self.grid_block_size + (i)*self.lines + self.screenBorderSize, self.height + self.screenBorderSize), self.lines)

		#Draw horizontal lines
		for i in range(self.gridSize + 1):
			pygame.draw.line(self.window, lineColour, (self.screenBorderSize,(i)*self.grid_block_size + (i)*self.lines + self.screenBorderSize),
				( self.height + self.screenBorderSize,(i)*self.grid_block_size + (i)*self.lines + self.screenBorderSize), self.lines)

		self.draw_cars()

		#Create the text for the move counter
		moves = self.font.render('Number of moves: ' + str(game.moveCount) ,False, textColour)
		self.window.blit(moves,(self.screenBorderSize / 4, self.screenBorderSize + self.height ))
		pygame.display.update()


	def draw_cars(self):
		'''
		A seperate function to draw the cars onto the screen.
		It distinguishes between the target car and the other cars by giving the target car a seperate colour (red).
		The function will not update the display by it's self because it is supposed to be called as part of the draw_board method.
		'''
		colour = (0,255,0)
		targetColour = (255,0,0)
		for car in Car.garage:

			if (car.name == 'A'): #The target car
				pygame.draw.rect(self.window ,targetColour ,[(self.screenBorderSize + (car.column * self.grid_block_size) + (car.column * self.lines) + self.lines ), (self.screenBorderSize + self.lines + (car.row*(self.grid_block_size+self.lines))),(car.length*(self.grid_block_size) + self.lines*(car.length - 2)),(self.grid_block_size - (self.lines))])

			elif (car.direction == 'h'):#Other horizontal cars
				pygame.draw.rect(self.window ,colour , [(self.screenBorderSize + (car.column * self.grid_block_size) + (car.column * self.lines) +self.lines),(self.screenBorderSize + self.lines + (car.row*(self.grid_block_size+self.lines))),(car.length*(self.grid_block_size) + self.lines*(car.length - 2)),(self.grid_block_size - (self.lines))])

			elif (car.direction == 'v'):#All of the vertical cars
				pygame.draw.rect(self.window ,colour ,[(self.screenBorderSize + (car.column * self.grid_block_size) + (car.column * self.lines) +self.lines),(self.screenBorderSize + self.lines + (car.row*(self.grid_block_size+self.lines))),(self.grid_block_size - (self.lines)),(car.length*(self.grid_block_size) + self.lines*(car.length - 2))])


	def select_position(self, position):
		'''
		The method used to determine what space a left click coresponds to on the grid.
		The method returns the values for the row,column in a tuple.
		If the click in the top or left border of the screen the method returns -1,-1 as the position
		This helps because the int function can round those problem spaces to 0 when it should be -1.
		'''
		xPos,yPos = position
		xGrid = int((xPos - self.screenBorderSize) / (self.grid_block_size + self.lines))
		yGrid = int((yPos - self.screenBorderSize) / (self.grid_block_size + self.lines))

		if (((xPos - self.screenBorderSize) < 0) or
			((yPos - self.screenBorderSize) < 0)):
			return -1,-1# The mouse click is inside the top / left border

		return (xGrid,yGrid)


	def mouse_down(self,position):
		'''
		The method that is called when a player left-clicks the screen.
		It will check if that player clicked on a car and will then move it to wherever they next click (if it is a valid move).
		The nested if statements in the loop are to check if the second click of the mouse is a valid target for a car to move to.
		'''
		selectX,selectY = self.select_position(position)

		if (selectY,selectX) in self.matrix:
			car = self.matrix[(selectY,selectX)]

			innerLoop = True
			while innerLoop:
				for ev in pygame.event.get():
					valid = False
					if (ev.type == pygame.QUIT):
						self.keepLooping = False
						self.innerLoop = False
					if (ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1):
						(moveToX,moveToY) = self.select_position(ev.pos)
						if car.direction == 'v':#vertical
							if (moveToX - selectX) == 0:#Must be along the same column
								spacesToMove = (moveToY - selectY)#The number of grid squares between the clicks.
								valid = True
						else:#horizontal
							if (moveToY - selectY) == 0:
								spacesToMove = (moveToX - selectX)
								valid = True
						if valid:
							car.move(spacesToMove)
						innerLoop = False


if __name__ == '__main__':
	game = Game()
	gui = Gui(game)
	gui.mainloop()
