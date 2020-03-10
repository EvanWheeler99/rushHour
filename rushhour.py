import sys
import string


class Game:
	'''
	The main class for the game.
	To run the game, create an instance of the game and then call it's mainloop method.
	'''

	moveCount = 0# used to count the number of moves made in a game

	def __init__(self):
	#Initializes the game and creates an instance of the board class
		self.board = Board()
		self.gridSize = self.board.gridSize
		if __name__ == '__main__':#So as to not execute during the gui game for no reason
			self.player = TerminalPlayer()


	def is_game_over(self):
		#Checks to see if there is a tile in the winning position
		if (2,self.board.gridSize) in self.board.matrix:
			return True
		else:
			return False


	def mainloop(self):
		'''
		The main game loop. As long as the game is not over it will continue looping.
		'''
		self.board.car_spawn()#Spawn the cars onto the board

		while not self.is_game_over():#Loops until the game ends

			self.board.print_state()

			selectedCar = self.player.choose_car_to_move()
			if selectedCar == None:
				print('Car not recognised')
				continue

			spacesToMove = self.player.choose_where_to_move()
			if spacesToMove == None:
				print('Invalid move')
				continue

			try:
				selectedCar.move(spacesToMove)
				# self.moveCount += 1
			except:
				print('Invalid move')
				continue
			# self.moveCount += 1
		#The game must be over to get this far
		self.board.print_state()
		print('Yay, you won!')
		print('You solved the puzzle in ' + str(self.moveCount) + ' moves.')


class Board:
	'''
	This class is used to represent the game board.
	It uses a dictionary to create a sparse matrix that uses a tuple (row,column) as the key to store the cars as values.
	'''
	gridSize = 6#The size of the game grid (6 by 6)

	def __init__(self):
		#Initializes the board as a sparse matrix
		self.matrix = self.make_matrix()
		self.lines = self.game_file_lines()


	def game_file_lines(self):
		#Takes the game file given by sys.argv and translates it into a nested list of lines
		text = str(sys.argv[1])
		text = open(text, 'r')
		lines = text.read()
		text.close()
		lines = lines.split('\n')

		for i in range(len(lines)):
			string = lines[i].split(', ')
			lines[i] = string
		return lines


	def make_matrix(self):
		#A simple method to create an enpty dictionary
		matrix = {}
		return matrix


	def car_spawn(self):
		#The method used to spawn the cars onto the board at the start of the game.
		for i in range(len(self.lines) - 1):#The example files have an empty last line and thus the need to not index into the last line
			direction = self.lines[i][0]
			length = int(self.lines[i][1])
			row = int(self.lines[i][2])
			column = int(self.lines[i][3])

			tempName = string.ascii_uppercase[i]#goes through the alphabet to name the cars
			tempName = Car(tempName, direction, length, row, column, self.matrix)
		return self


	def print_state(self):
		'''
		This is the method used to print the state of the board in the text based game.
		The border of the game is made up of '*' characters and all empty spaces are left blank.
		Any car in the matrix is shown by it's name in all the spots it occupies.
		'''

		for i in range(self.gridSize + 1):
			print('*', end='  ')
		print('*')

		rowCount = 0
		for row in range(self.gridSize):
			print('*', end=' ')
			for col in range (self.gridSize):
				if (row,col) in self.matrix:
					print('', end=' ')#to help space out the columns
					print (self.matrix[row,col],end=' ')
				else:
					print ('   ',end='')
			if rowCount != 2:
				print(' *')#For a new line after every row
			else:
				if (2,self.gridSize) in self.matrix:
					print('',end=' ')
					print (self.matrix[2,self.gridSize],end=' ')
				else:
					print ('   ',end='')
				print(' *')# This will be the row that the target car is on.
			rowCount += 1

		for i in range(self.gridSize + 1):
			print('*', end='  ')
		print('*')


class Car:
	'''
	The car class. All of the cars on the board are instances of this class.
	'''
	garage = []# A list containing all of the instances of the car class

	def __init__(self, name, direction, length, row, column, matrix):
		#Initializes a car given several specifications
		self.name = name
		self.direction = direction#'h' or 'v'
		self.length = length
		self.row = row#Top left
		self.column = column#Top left
		self.matrix = matrix

		self.occupies = []#a list of all the spaces the car occupies
		self.add_to_matrix()

		self.garage.append( self )# Puts the car into the garage up in the hollywood hills


	def __str__(self):
		#Used so that calling print(car) gives the name of the car and not something like <an instance of Car at ....>
		return (self.name)


	def move(self, spacesToMove ):
		'''
		To move a car, first the move is checked to see if it is legal.
		Then the car is removed from the garage and a new one is made in the desired spot with the same name.
		'''
		if (self.is_not_off_board(spacesToMove)) and (self.is_no_collision(spacesToMove)):
			# This is a valid move
			self.occupies = []
			self.garage.remove(self)

			for i in range (self.length):
				if self.direction == 'v':
					del self.matrix[(self.row + i, self.column)]
				else:
					del self.matrix[(self.row, self.column + i)]


			if self.direction == 'v':
				movedCar = Car( self.name, self.direction, self.length, (self.row + spacesToMove), self.column, self.matrix)
			else:# Horizontal
				movedCar = Car( self.name, self.direction, self.length, self.row, (self.column + spacesToMove), self.matrix)

			if spacesToMove != 0:
				Game.moveCount += 1# add one to the variable counting the number of moves made


	def is_not_off_board(self, spacesToMove):
		'''
		A function that will test to see if a desired move would move the car off screen
		If the target car is the car in question and it chooses to go right the check
		will come back true (it needs to for the player to be able to win).
		'''
		if self.direction == 'v':# Vertical
			if spacesToMove < 0:# Up
				if (self.row - abs(spacesToMove)) < 0:
					return False
			if spacesToMove > 0:# Down
				if (self.row + (self.length - 1) + abs(spacesToMove)) > (Board.gridSize - 1):
					return False

		else:# Horizontal
			if spacesToMove < 0:# Left
				if (self.column - abs(spacesToMove)) < 0:
					return False
			if spacesToMove > 0:# Right
				if self.name != 'A':# The target car must be able to go off the right
									#side of the grid to win the game.
					if (self.column + (self.length - 1) + abs(spacesToMove)) > (Board.gridSize - 1):
						return False
				else:
					if (self.column + (self.length - 1) + abs(spacesToMove)) > (Board.gridSize):
						return False

		return True# will only execute if all the tests pass


	def is_no_collision(self, spacesToMove):
		'''
		A function to test if the move will cause cars to crash.
		It uses a series of nested if's dependant on the orientation of the car
		and the desired direction of movement.
		It will return false if the car would try to move into an occupied space and only return True if the whole path is clear.
		Input of 0 in a direction would still yield true because a car will not
		crash if it doesn't move.
		'''
		if self.direction == 'v':# Vertical
			if spacesToMove < 0:# Up
				for i in range(1, abs(spacesToMove) + 1):# We want to start at 1
					if (self.row - i, self.column) in self.matrix:
						return False
			if spacesToMove > 0:# Down
				for i in range(1, abs(spacesToMove) + 1):# We want to start at 1
					if (self.row + (self.length - 1) + i, self.column) in self.matrix:
						return False

		else:# Horizontal
			if spacesToMove < 0:# Left
				for i in range(1, abs(spacesToMove) + 1):# We want to start at 1
					if (self.row, self.column - i) in self.matrix:
						return False
			if spacesToMove > 0:# Right
				for i in range(1, abs(spacesToMove) + 1):# We want to start at 1
					if (self.row, self.column+ (self.length - 1) + i) in self.matrix:
						return False
		return True# will only execute if all the tests pass


	def add_to_matrix(self):
		'''Adds the car into the sparse matrix with the key being its position (row, column).
		Then it adds that same tuple into a list called self.occupies to keep track of which spaces the car occupies'''

		if self.direction == 'h':
			for j in range(self.length):
				self.matrix[(self.row , (self.column + j))] = self
				self.occupies.append((self.row , (self.column + j)))

		elif self.direction == 'v':
			for j in range(self.length):
				self.matrix[((self.row + j) , self.column)] = self
				self.occupies.append(((self.row + j) , self.column))

		return self


class TerminalPlayer:
	'''
	A class that controls all of the palayer input in a text-based game
	'''
	terminalGame = False
	def __init__(self):
		#If an instance is created then terminalGame will be True, mostly for debuging
		self.terminalGame = True


	def choose_car_to_move(self):
		#The input for choosing which car to move
		carToMove = input('Select a car to move.(Enter the letter of the car): ')
		try:
			carToMove = carToMove.upper()
		except:
			return None

		valid = False
		for car in Car.garage:
			if carToMove == car.name:
				valid = True
				carObject = car
				return carObject

		if valid == False:
			return None


	def choose_where_to_move(self):
		#The input for choosing where to move the car.
		spacesToMove = input('Choose where to move the car.\n (negative numbers move (up/ left) and positive numbers move (down/ right) ): ')
		try:
			spacesToMove = int(spacesToMove)
		except:
			# print('Try again. (The number must be an integer)')
			# return self.choose_where_to_move()
			return None
		return spacesToMove


if __name__ == '__main__':
	game = Game()
	game.mainloop()
