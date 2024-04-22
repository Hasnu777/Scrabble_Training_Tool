import pygame as pg
import os
import random
# List holding all playable letters, for English/French/Spanish
AllScrabbleLetters = ['!', 'A', 'B', 'C', 'CH', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'LL', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'RR', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Lists to hold: the amount of each letter in the tile bag, the score of each letter.
EnglishQuantities = [2, 9, 2, 2, None, 4, 12, 2, 3, 2, 9, 1, 1, 4, None, 2, 6, None, 8, 2, 1, 6, None, 4, 6, 4, 2, 2, 1, 2, 1]
EnglishScore = [0, 1, 3, 3, None, 2, 1, 4, 2, 4, 1, 8, 5, 1, None, 3, 1, None, 1, 3, 10, 1, None, 1, 1, 1, 4, 4, 8, 4, 10]

# Dictionary with each letter in English Scrabble as the key, and a tuple of the score and quantity as the value IF a value is stored
EnglishLetters = {letter: (score, quantity) for letter, score, quantity in zip(AllScrabbleLetters, EnglishScore, EnglishQuantities) if (score is not None and quantity is not None)}

# Lists to hold: the amount of each letter in the tile bag, the score of each letter.
FrenchQuantities = [0, 9, 2, 2, None, 3, 15, 2, 2, 2, 8, 1, 1, 5, None, 3, 6, None, 6, 2, 1, 6, None, 6, 6, 6, 2, 1, 1, 1, 1]
FrenchScore = [0, 1, 3, 3, None, 2, 1, 4, 2, 4, 1, 8, 10, 1, None, 2, 1, None, 1, 3, 8, 1, None, 1, 1, 1, 4, 10, 10, 10, 10]

# Dictionary with each letter in French Scrabble as the key, and a tuple of the score and quantity as the value IF a value is stored
FrenchLetters = {letter: (score, quantity) for letter, score, quantity in zip(AllScrabbleLetters, FrenchScore, FrenchQuantities) if (score is not None and quantity is not None)}

# Lists to hold: the amount of each letter in the tile bag, the score of each letter.
SpanishQuantities = [2, 12, 2, 4, 1, 5, 12, 1, 2, 2, 6, 1, None, 4, 1, 2, 5, 1, 9, 2, 1, 5, 1, 6, 4, 5, 1, None, 1, 1, 1]
SpanishScore = [0, 1, 3, 3, 5, 2, 1, 4, 2, 4, 1, 8, None, 1, 8, 3, 1, 8, 1, 3, 5, 1, 8, 1, 1, 1, 4, None, 8, 4, 10]
# Dictionary with each letter in Spanish Scrabble as the key, and a tuple of the score and quantity as the value IF a value is stored
SpanishLetters = {letter: (score, quantity) for letter, score, quantity in zip(AllScrabbleLetters, SpanishScore, SpanishQuantities) if (score is not None and quantity is not None)}

# Dictionary with each premium square type as the key & a list of x-y coordinate pairs for their locations on the board
SpecialLocations = {
			'TW': [(0, 0), (0, 7), (0, 14), (7, 0), (14, 0), (14, 7), (14, 14), (7, 14)],
			'DW': [(1, 1), (2, 2), (3, 3), (4, 4), (4, 10), (3, 11), (2, 12), (1, 13), (7, 7), (13, 1), (12, 2), (11, 3), (10, 4), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14)],
			'TL': [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9)],
			'DL': [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (6, 6), (6, 8), (6, 12), (7, 3), (7, 11), (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)]
		}

REGULAR_TIME = 1500  # 25 minutes / 1500 seconds
OVERTIME_TIME = 600  # 10 minutes / 600 seconds


# Used to create tiles for the players. Maximum of 100 for English/Spanish games, or 102 for French games.
class Tile(pg.sprite.Sprite):
	def __init__(self, filename, coordinates, letter, score):
		super().__init__()
		# Loads in image from the assets folder
		self.image = pg.image.load(os.path.join(os.path.dirname(__file__), f'../assets\\images\\{filename}'))
		# Gets a clickable area the size of the image, and place the top-left of this rect at the specified location
		self.rect = self.image.get_rect(topleft=coordinates)
		self.__letter = letter
		self.__score = score
		self.isClicked = False
		self.canBeClicked = True

	# Moves the rect to a new location
	def updateRect(self, coordinates):
		self.rect = self.image.get_rect().move(coordinates[0], coordinates[1])

	# Gets the coordinates of the rect (default is coordinates of top-left of rect)
	def getRectCoordinates(self):
		return self.rect.x, self.rect.y

	# Returns the Rect() object
	def getRect(self):
		return self.rect

	# Loads in a new image, specified by the filename parameter
	def updateImage(self, filename):
		self.image = pg.image.load(os.path.join(os.path.dirname(__file__), f'../assets\\images\\{filename}'))

	# Changes the size of the image to the given size
	def transformImage(self, size):
		self.image = pg.transform.scale(self.image, size)

	# Returns the image object
	def getImage(self):
		return self.image

	# Updates the letter
	def updateLetter(self, letter):
		self.__letter = letter

	# Returns the letter
	def getLetter(self):
		return self.__letter

	# Returns the score
	def getScore(self):
		return self.__score


# Used to create a single 1 Board object
class Board(pg.sprite.Sprite):
	def __init__(self, coordinates):
		super().__init__()
		self.__board = [[' ' for _ in range(15)] for __ in range(15)]  # Creates 2D array of the board
		# Loads in image of the game board from the assets folder
		self.__image = pg.image.load(os.path.join(os.path.dirname(__file__),
												f'../assets\\images\\GameBoard.png')).convert_alpha()
		# Gets a clickable area the size of the image, and place the top-left of this rect at the specified location
		self.__rect = self.__image.get_rect(topleft=coordinates)
		# Creates a 2D array of Square objects, to make the board squares clickable and to represent premium squares
		self.squares = [[Square(((448+j*48), (58+i*48)), text=' ') for j in range(15)] for i in range(15)]
		self.__group = pg.sprite.Group()  # Used to display Sprite objects that represent tiles/squares on the board.

	def updateRect(self, coordinates):
		self.__rect.move(coordinates[0], coordinates[1])

	def getRectCoordinates(self):
		return self.__rect.x, self.__rect.y

	def transformImage(self, size):
		self.__image = pg.transform.scale(self.__image, size)  # changes the size of the image to the given size

	def getImage(self):
		return self.__image  # Returns the image object

	def replaceBoard(self, board):
		self.__board = board  # Updates the board

	def addToBoard(self, row, column, letter):
		self.__board[row][column] = letter  # Adds a leter to the board

	def getBoard(self):
		return self.__board  # Returns the 2D board array

	def addToGroup(self, sprite):
		self.__group.add(sprite)  # Adds the sprite to the board's group, so it can be displayed on the game window

	def removeFromGroup(self, sprite):
		self.__group.remove(sprite)  # Removes the sprite from the board's group

	def getGroup(self):
		return self.__group  # Returns the group of the board

	def CheckForSpecialLocation(self, row, column):
		return self.__board[row][column]


# Used to create 2 Rack objects, one per player
class Rack(pg.sprite.Sprite):
	def __init__(self, coordinates):
		super().__init__()
		# Loads in image of the rack from the assets folder
		self.__image = pg.image.load(os.path.join(os.path.dirname(__file__), f'../assets\\images\\DeckFront.png'))
		# Gets a clickable area the size of the image, and place the top-left of this rect at the specified location
		self.__rect = self.__image.get_rect(topleft=coordinates)
		self.__contents = ['' for _ in range(7)]  # Stores the actual letters in the rack
		# Stores the Tile objects that represent each letter in self.__contents
		self.__sprites = {
			'TILE1': None,
			'TILE2': None,
			'TILE3': None,
			'TILE4': None,
			'TILE5': None,
			'TILE6': None,
			'TILE7': None
			}
		self.__group = pg.sprite.Group()  # Used to display Tile objects that represent letters in the rack

	# Moves the rect to the specified location
	def updateRect(self, coordinates):
		self.__rect.move(coordinates[0], coordinates[1])

	# Returns the coordinates of the rect
	def getRectCoordinates(self):
		return self.__rect.x, self.__rect.y

	# Updates the image by changing its size to the given size
	def transformImage(self, size):
		self.__image = pg.transform.scale(self.__image, size)

	# Returns the image object
	def getImage(self):
		return self.__image

	# Updates the actual rack
	def replaceContents(self, contents):
		self.__contents = contents

	# Returns the rack
	def getContents(self):
		return self.__contents

	# Updates the sprite dictionary of the rack
	def updateSprites(self, sprites):
		self.__sprites = sprites

	# This is used to display the tiles of the other player's rack, when a game is over. If Player 1 just played, this
	# gets called for Player 2 and vice versa.
	def alterSprites(self):
		self.__group.empty()  # Removes all Tile objects from the group
		for i in range(7):  # Definite iterative loop to go through each rack position
			# Gets the value of the rack position's sprite (or None if no sprite exists)
			tile = self.__sprites[f'TILE{i+1}']
			if tile is not None:  # Checks to see if a Tile object was actually retrieved
				self.__sprites[f'TILE{i+1}'] = tile.updateRect((1084+i*64, 798))  # Moves the rect of the sprite
				self.__group.add(tile)  # Adds the tile object back to the group

	# Returns the sprite dictionary for the rack
	def getSprites(self):
		return self.__sprites

	# Fills up the rack with tiles from the tile bag
	def fillRack(self, tileBag):
		print('filling rack')
		# Checks if there are empty spots in the rack AND if there are tiles in the tile bag
		# Indefinite iterative loop used due to random selection of letters
		while '' in self.__contents and not tileBag.isEmpty():
			print('entered while loop')
			letters = tileBag.bag[:-1]  # Removes the isEmpty() flag from the bag array of the TileBag object
			letter = random.choice(letters)  # Picks out a random letter from the tile bag
			indexPosition = tileBag.bag.index(letter)  # Takes the index position of the letter in the bag array
			if tileBag.bag[indexPosition][2] > 0:  # Checks if there are any available tiles left for that letter
				self.__contents[self.__contents.index('')] = letter[0]  # Puts that letter in the rack
				# Updates the letter information to show a tile's been removed from the rack
				tileBag.bag[indexPosition] = (letter[0], letter[1], (letter[2] - 1))
				if letter[2] - 1 == 0:  # Checks if all tiles for that letter are gone from the tile bag
					tileBag.bag[-1] += 1  # Updates the isEmpty() flag of the bag array accordingly

	# Adds a tile to the Rack object
	def addToRack(self, position, tile):
		self.__contents[position] = tile.getLetter()  # Adds the tile's letter to the rack
		self.__sprites[f'TILE{position+1}'] = tile  # Adds the tile to the sprites dictionary
		self.__group.add(tile)  # Adds the tile to the rack's group

	# Removes a tile from the Rack object
	def removeFromRack(self, position, tile):
		self.__contents[position] = ''  # Removes the letter from the rack
		self.__sprites[f'TILE{position+1}'] = None  # Removes the tile object from the sprites dictionary
		self.__group.remove(tile)  # Removes the tile object from the rack's group

	# Takes the rack and creates Tile objects, to add to the rack's group
	def fillRackGroup(self, language, lexicon):
		self.__group.empty()  # Removes all tiles from the group
		for i, letter in enumerate(self.__contents):  # Definite iterative loop to go over each letter in the rack
			if self.__sprites[f'TILE{i+1}'] is None and letter != '':  # Checks if a letter exists in the rack
				# Gets the image of the letter's tile for the game version
				filename = f'{language}Letters\\TILE_{letter}.png'
				# Creates coordinates for each tile, iterating through each rack's tile slot
				coordinates = (584+i*64, 798)
				score = lexicon[letter][0]  # Gets the score of the letter
				# Creates and adds a Tile object to the sprites dictionary
				self.__sprites[f'TILE{i+1}'] = Tile(filename, coordinates, letter, score)
				print(f'added sprite number {i+1} to __sprites')
				self.__group.add(self.__sprites[f'TILE{i + 1}'])  # Adds the Tile object to the rack's Group
				print(f'added sprite number {i+1} to __group. If you find no errors, remove the extra comments')
			# if self.__sprites[f'TILE{i+1}'] is not None:  # Checks if a Tile object has been added to the sprite dictionary
			# 	self.__group.add(self.__sprites[f'TILE{i+1}'])  # Adds the Tile object to the rack's Group

	# Puts Sprite objects in the group onto the window
	def drawGroup(self, surface):
		self.__group.draw(surface)

	# Returns the group
	def getGroup(self):
		return self.__group

	# Gets the point value of the entire rack, and returns twice that.
	# Used to award final scores after a game is over, if applicable.
	def getTotalScore(self, lexicon):
		score = 0
		for letter in self.__contents:  # Selects each letter in the rack
			score += lexicon[letter][0]  # Retrieves the score of each letter from the language's lexicon
		return 2 * score  # Returns double the score calculated

	# Returns a Boolean variable to show if the rack is empty or not
	def isEmpty(self):
		return self.__contents.count('') == 7  # If there are no tiles left, this returns True. Else, False.


# Command to fill the tile bag up at the beginning of a game
def fillBag(lexicon):
	tile_bag = []
	for letter in lexicon.keys():  # Goes through each letter available for the game
		# Creates a tuple of the letter, its score, and its quantity then appends this tuple to the tile bag
		tile_bag.append((letter, lexicon[letter][0], lexicon[letter][1]))
	random.shuffle(tile_bag)
	tile_bag.append(0)  # Adds the isEmpty() flag to the tile bag
	return tile_bag  # Returns the tile bag


# Used to create a single TileBag object
class TileBag(pg.sprite.Sprite):
	def __init__(self, coordinates, language):
		super().__init__()
		# Loads in image of the tile bag from the assets folder
		self.__image = pg.image.load(os.path.join(os.path.dirname(__file__),
									'../assets\\images\\TileBag.png')).convert_alpha()
		# Gets a clickable area the size of the image, and place the top-left of this rect at the specified location
		self.__rect = self.__image.get_rect(topleft=coordinates)
		# Stores the language type of the game
		self.__language = language
		# Stores how many times the tile bag has been shuffled
		self.shuffleCount = 0

		# Match-case used to check the language of the game to fill the tile bag accordingly
		# Also stores the correct alphabet and lexicon in the Tile Bag object
		match self.__language:
			case 'English':
				self.bag = fillBag(EnglishLetters)
				self.alphabet = list(EnglishLetters.keys())  # Gets a list of all the English Scrabble letters
				self.lexicon = EnglishLetters
			case 'French':
				self.bag = fillBag(FrenchLetters)
				self.alphabet = list(FrenchLetters.keys())  # Gets a list of all the French Scrabble letters
				self.lexicon = FrenchLetters
			case 'Spanish':
				self.bag = fillBag(SpanishLetters)
				self.alphabet = list(SpanishLetters.keys())  # Gets a list of all the Spanish Scrabble letters
				self.lexicon = SpanishLetters
			case _:
				self.bag = fillBag(EnglishLetters)
				self.alphabet = list(EnglishLetters.keys())  # Gets a list of all the English Scrabble letters
				self.lexicon = EnglishLetters

	# Moves the rect to the specified location
	def updateRect(self, coordinates):
		self.__rect.move(coordinates[0], coordinates[1])

	# Returns the coordinates of the rect
	def getRectCoordinates(self):
		return self.__rect.x, self.__rect.y

	# Updates the image by changing its size to the given size
	def transformImage(self, size):
		self.__image = pg.transform.scale(self.__image, size)

	# Returns the image object
	def getImage(self):
		return self.__image

	# Updates the bag array
	def replaceBag(self, bag):
		self.bag = bag

	# Randomises the order of the letters in the bag array
	def shuffleBag(self):
		if self.shuffleCount < 2:  # Checks if each player has shuffled the tile bag
			lettersInBag = self.bag[:-1]  # Removes the isEmpty() flag from the bag array
			emptyLetters = self.bag[-1]  # Takes the isEmpty() flag of the bag array
			random.shuffle(lettersInBag)  # Randomises the order of the letters only
			self.bag = lettersInBag  # Updates the bag array to be the randomised list of letters
			self.bag.append(emptyLetters)  # Adds the flag array to the bag
			self.shuffleCount += 1

	# Returns the language of the game i.e. 'English', 'French', or 'Spanish'
	def getLanguage(self):
		return self.__language

	# Returns a Boolean value showing if the isEmpty() flag is the same as the number of letters in the Scrabble game
	def isEmpty(self):
		return self.bag[-1] == len(self.bag)-1


# Used to create 2 Player objects, one per player
class Player:
	def __init__(self, name, rackCoordinates, scoreCoordinates, timerCoordinates):
		self.name = name  # Stores the name of the player
		self.rack = Rack(rackCoordinates)  # Creates a Rack object for the player
		self.score = Score(scoreCoordinates)  # Creates a Score object for the player
		self.timer = Timer(REGULAR_TIME, timerCoordinates)  # Creates a Timer object for the player

	# Replaces the regular timer with an overtime timer and updates the isOvertime flag
	def replaceTimer(self):
		# Creates a new Timer object and takes the rect coordinates of the old timer, to use for the new timer.
		self.timer = Timer(OVERTIME_TIME, (self.timer.getRectCoordinates()))
		self.timer.isOvertime = True


# Used to create 2 Timer objects, one per player
class Timer:
	def __init__(self, initialSeconds, coordinates):
		# Creates a font object, with Helvetica as the font
		self.font = pg.font.Font(os.path.join(os.path.dirname(__file__),
												'../assets\\Helvetica-Font\\Helvetica.ttf'), 24)
		self.current_seconds = initialSeconds  # Sets the timer
		# Renders the text to display the timer
		self.text = self.font.render(f"Time Left: {self.current_seconds // 60:02}:{self.current_seconds % 60:02}",
									True, 'white')
		# Creates a rect object for the timer
		self.__rect = self.text.get_rect(topleft=coordinates)
		self.isOvertime = False  # Default overtime flag should be False, all players start with regular time.

	# Moves the rect to the specified coordinates
	def updateRect(self, coordinates):
		self.__rect.move(coordinates[0], coordinates[1])

	# Returns the rect coordinates
	def getRectCoordinates(self):
		return self.__rect.x, self.__rect.y

	# Updates the text displayed to represent the regular timer
	def updateTimer(self):
		self.text = self.font.render(f"Time Left: {self.current_seconds // 60:02}:{self.current_seconds % 60:02}",
									True, 'white')

	# Updates the text displayed to represent the overtime timer
	def updateOvertimeTimer(self):
		self.text = self.font.render(f"Time Left (Overtime): {self.current_seconds // 60:02}:\
									{self.current_seconds % 60:02}", True, 'white')


# Used to create 2 Score objects, one per player
class Score:
	def __init__(self, coordinates):
		self.__score = 0
		# Creates a font object, with Helvetica as the font
		self.font = pg.font.Font(os.path.join(os.path.dirname(__file__),
											'../assets\\Helvetica-Font\\Helvetica.ttf'), 24)
		# Renders the text to display the score
		self.text = self.font.render(f'Score: {self.__score}', True, 'white')
		# Creates a rect object for the score
		self.__rect = self.text.get_rect(topleft=coordinates)

	# Moves the rect to the specified coordinates
	def updateRect(self, coordinates):
		self.__rect.move(coordinates[0], coordinates[1])

	# Returns the rect coordinates
	def getRectCoordinates(self):
		return self.__rect.x, self.__rect.y

	# Updates the score
	def updateScore(self, score):
		self.__score += score
		self.updateText()  # Called to automatically update the text

	def getScore(self):
		return self.__score

	# Updates the text to reflect the updated score
	def updateText(self):
		self.text = self.font.render(f'Score: {self.__score}', True, 'white')


# Used to create Text objects to display messages/information
class Text:  # Turn this into square, and alter it so if a tile is passed in then that gets put in I guess, smth like that
	def __init__(self, coordinates, size, text):
		# Creates a Font object with Helvetica as the font
		self.font = pg.font.Font(os.path.join(os.path.dirname(__file__),
											'../assets\\Helvetica-Font\\Helvetica.ttf'), 14)
		# Renders the font to display the message
		self.text = self.font.render(f'{text}', True, 'white')
		# Creates a Rect with the given coordinates
		self.rect = pg.Rect(coordinates, size)

	# Used to update the text
	def updateText(self, text):
		self.text = self.font.render(f'{text}', True, 'white')


# Used to create 225 Square objects, one for each square on a Scrabble board
class Square:
	def __init__(self, coordinates, text=' '):
		# Used to create a Font object with Helvetica as the font
		self.__font = pg.font.Font(os.path.join(os.path.dirname(__file__), '../assets\\Helvetica-Font\\Helvetica.ttf'), 16)
		# Used to render the text of the square
		self.__text = self.__font.render(f'{text}', True, 'white')
		# Gets the rect of the text
		self.__rect = pg.Rect((coordinates[0], coordinates[1]), (32, 32))
		self.squareType = text  # Gets the text to display for the square, to show the type of premium square

	# Returns the rect
	def getSquareRect(self):
		return self.__rect

	# Returns the rect coordinates
	def getRectCoordinates(self):
		return self.__rect.x, self.__rect.y

	# Returns the rendered text of the square
	def getText(self):
		return self.__text

	# Returns the square type
	def getType(self):
		return self.squareType
