import pygame as pg
import os
import random

AllScrabbleLetters = ['!', 'A', 'B', 'C', 'CH', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'LL', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'RR', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

EnglishQuantities = [2, 9, 2, 2, None, 4, 12, 2, 3, 2, 9, 1, 1, 4, None, 2, 6, None, 8, 2, 1, 6, None, 4, 6, 4, 2, 2, 1, 2, 1]
EnglishScore = [0, 1, 3, 3, None, 2, 1, 4, 2, 4, 1, 8, 5, 1, None, 3, 1, None, 1, 3, 10, 1, None, 1, 1, 1, 4, 4, 8, 4, 10]
EnglishLetters = {letter: (score, quantity) for letter, score, quantity in zip(AllScrabbleLetters, EnglishScore, EnglishQuantities) if (score is not None and quantity is not None)}

FrenchQuantities = [0, 9, 2, 2, None, 3, 15, 2, 2, 2, 8, 1, 1, 5, None, 3, 6, None, 6, 2, 1, 6, None, 6, 6, 6, 2, 1, 1, 1, 1]
FrenchScore = [0, 1, 3, 3, None, 2, 1, 4, 2, 4, 1, 8, 10, 1, None, 2, 1, None, 1, 3, 8, 1, None, 1, 1, 1, 4, 10, 10, 10, 10]
FrenchLetters = {letter: (score, quantity) for letter, score, quantity in zip(AllScrabbleLetters, FrenchScore, FrenchQuantities) if (score is not None and quantity is not None)}

SpanishQuantities = [2, 12, 2, 4, 1, 5, 12, 1, 2, 2, 6, 1, None, 4, 1, 2, 5, 1, 9, 2, 1, 5, 1, 6, 4, 5, 1, None, 1, 1, 1]
SpanishScore = [0, 1, 3, 3, 5, 2, 1, 4, 2, 4, 1, 8, None, 1, 8, 3, 1, 8, 1, 3, 5, 1, 8, 1, 1, 1, 4, None, 8, 4, 10]
SpanishLetters = {letter: (score, quantity) for letter, score, quantity in zip(AllScrabbleLetters, SpanishScore, SpanishQuantities) if (score is not None and quantity is not None)}

SpecialLocations = {
			'TW': [(0, 0), (0, 7), (0, 14), (7, 0), (14, 0), (14, 7), (14, 14), (7, 14)],
			'DW': [(1, 1), (2, 2), (3, 3), (4, 4), (4, 10), (3, 11), (2, 12), (1, 13), (7, 7), (13, 1), (12, 2), (11, 3), (10, 4), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14)],
			'TL': [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9)],
			'DL': [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (6, 6), (6, 8), (6, 12), (7, 3), (7, 11), (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)]
		}

REGULAR_TIME = 1500  # 25 minutes / 1500 seconds
OVERTIME_TIME = 600  # 10 minutes / 600 seconds


class Tile(pg.sprite.Sprite):
	def __init__(self, filename, coordinates, letter, score):
		super().__init__()
		self.image = pg.image.load(os.path.join(os.path.dirname(__file__), f'../assets\\images\\{filename}'))
		self.rect = self.image.get_rect().move(coordinates[0], coordinates[1])
		self.__letter = letter
		self.__score = score
		self.isClicked = False
		self.canBeClicked = True

	def updateRect(self, coordinates):
		self.rect = self.image.get_rect().move(coordinates[0], coordinates[1])

	def getRectCoordinates(self):
		return self.rect.x, self.rect.y

	def getRect(self):
		return self.rect

	def transformImage(self, size):
		self.image = pg.transform.scale(self.image, size)

	def getImage(self):
		return self.image

	def getLetter(self):
		return self.__letter

	def updateLetter(self, letter):
		self.__letter = letter

	def updateImage(self, filename):
		self.image = pg.image.load(os.path.join(os.path.dirname(__file__), f'../assets\\images\\{filename}'))

	def getScore(self):
		return self.__score


class Board(pg.sprite.Sprite):
	def __init__(self, coordinates):
		super().__init__()
		self.__board = [[' ' for _ in range(15)] for __ in range(15)]
		self.__image = pg.image.load(os.path.join(os.path.dirname(__file__), f'../assets\\images\\GameBoard.png')).convert_alpha()
		self.__rect = self.__image.get_rect(topleft=coordinates)
		self.squares = [[Square(((448+j*48), (58+i*48)), text=' ') for j in range(15)] for i in range(15)]
		self.__group = pg.sprite.Group()

	def transformImage(self, size):
		self.__image = pg.transform.scale(self.__image, size)

	def getImage(self):
		return self.__image

	def updateRect(self, coordinates):
		self.__rect.move(coordinates[0], coordinates[1])

	def getRectCoordinates(self):
		return self.__rect.x, self.__rect.y

	def CheckForSpecialLocation(self, row, column):
		return self.__board[row][column]

	def addToGroup(self, sprite):
		self.__group.add(sprite)

	def removeFromGroup(self, sprite):
		self.__group.remove(sprite)

	def addToBoard(self, row, column, letter):
		self.__board[row][column] = letter

	def getGroup(self):
		return self.__group

	def getBoard(self):
		return self.__board


class Rack(pg.sprite.Sprite):
	def __init__(self, coordinates):
		super().__init__()
		self.__image = pg.image.load(os.path.join(os.path.dirname(__file__), f'../assets\\images\\DeckFront.png'))
		self.__rect = self.__image.get_rect(topleft=coordinates)
		self.__contents = ['' for i in range(7)]
		self.__sprites = {'TILE1': None, 'TILE2': None, 'TILE3': None, 'TILE4': None, 'TILE5': None, 'TILE6': None, 'TILE7': None}
		self.__group = pg.sprite.Group()

	def transformImage(self, size):
		self.__image = pg.transform.scale(self.__image, size)

	def getImage(self):
		return self.__image

	def updateRect(self, coordinates):
		self.__rect.move(coordinates[0], coordinates[1])

	def getRectCoordinates(self):
		return self.__rect.x, self.__rect.y

	def fillRack(self, tileBag):
		while '' in self.__contents and not tileBag.isEmpty():
			letters = tileBag.bag[:-1]
			letter = random.choice(letters)
			indexPosition = tileBag.bag.index(letter)
			if tileBag.bag[indexPosition][2] > 0:
				self.__contents[self.__contents.index('')] = letter[0]
				tileBag.bag[indexPosition] = (letter[0], letter[1], (letter[2] - 1))
				if letter[2] - 1 == 0:
					tileBag.bag[-1] += 1

	def fillRackGroup(self, language, lexicon):
		self.__group.empty()
		for i, letter in enumerate(self.__contents):
			if self.__sprites[f'TILE{i+1}'] is None:
				filename = f'{language}Letters\\TILE_{letter}.png'
				coordinates = (584+i*64, 798)
				score = lexicon[letter][0]
				self.__sprites[f'TILE{i+1}'] = Tile(filename, coordinates, letter, score)
			self.__group.add(self.__sprites[f'TILE{i+1}'])

	def drawGroup(self, surface):
		self.__group.draw(surface)

	def getGroup(self):
		return self.__group

	def getContents(self):
		return self.__contents

	def getSprites(self):
		return self.__sprites

	def updateSprites(self, sprites):
		self.__sprites = sprites


	def removeFromRack(self, position, tile):
		self.__contents[position] = ''
		self.__sprites[f'TILE{position+1}'] = None
		self.__group.remove(tile)

	def addToRack(self, position, tile):
		self.__contents[position] = tile.getLetter()
		self.__sprites[f'TILE{position+1}'] = tile
		self.__group.add(tile)


def fillBag(lexicon):
	tile_bag = []
	for letter in lexicon.keys():
		tile_bag.append((letter, lexicon[letter][0], lexicon[letter][1]))
	tile_bag.append(0)
	return tile_bag


class TileBag(pg.sprite.Sprite):
	def __init__(self, coordinates, language):
		super().__init__()
		self.__image = pg.image.load(os.path.join(os.path.dirname(__file__), '../assets\\images\\TileBag.png')).convert_alpha()
		self.__rect = self.__image.get_rect(topleft=coordinates)
		self.__language = language
		self.shuffleCount = 0

		match self.__language:
			case 'English':
				self.bag = fillBag(EnglishLetters)
				self.alphabet = list(EnglishLetters.keys())
				self.lexicon = EnglishLetters
			case 'French':
				self.bag = fillBag(FrenchLetters)
				self.alphabet = list(FrenchLetters.keys())
				self.lexicon = FrenchLetters
			case 'Spanish':
				self.bag = fillBag(SpanishLetters)
				self.alphabet = list(SpanishLetters.keys())
				self.lexicon = SpanishLetters
			case _:
				self.bag = fillBag(EnglishLetters)
				self.alphabet = list(EnglishLetters.keys())
				self.lexicon = EnglishLetters

	def transformImage(self, size):
		self.__image = pg.transform.scale(self.__image, size)

	def getImage(self):
		return self.__image

	def updateRect(self, coordinates):
		self.__rect.move(coordinates[0], coordinates[1])

	def getRectCoordinates(self):
		return self.__rect.x, self.__rect.y

	def shuffleBag(self):
		if self.shuffleCount < 2:
			lettersInBag = self.bag[:-1]
			emptyLetters = self.bag[-1]
			random.shuffle(lettersInBag)
			self.bag = lettersInBag
			self.bag.append(emptyLetters)
			self.shuffleCount += 1

	def isEmpty(self):
		return self.bag[-1] == len(self.bag)-1

	def getLanguage(self):
		return self.__language

	def unknown(self):
		pass


class Player:
	def __init__(self, rackCoordinates, scoreCoordinates, timerCoordinates):
		self.rack = Rack(rackCoordinates)
		self.score = Score(scoreCoordinates)
		self.__penalties = 0
		self.timer = Timer(REGULAR_TIME, timerCoordinates)

	def getPenalties(self):
		return self.__penalties

	def updatePenalties(self, penalty):
		self.__penalties += penalty

	def replaceTimer(self):
		self.timer = Timer(OVERTIME_TIME, (self.timer.getRectCoordinates()))

	def unknown(self):
		pass


class Timer:
	def __init__(self, initialSeconds, coordinates):
		self.font = pg.font.Font(os.path.join(os.path.dirname(__file__), '../assets\\Helvetica-Font\\Helvetica.ttf'),24)
		self.current_seconds = initialSeconds
		self.text = self.font.render(f"Time Left: {self.current_seconds // 60:02}:{self.current_seconds % 60:02}", True, 'white')
		self.__rect = self.text.get_rect(topleft=coordinates)
		self.isOvertime = False

	def updateTimer(self):
		self.text = self.font.render(f"Time Left: {self.current_seconds // 60:02}:{self.current_seconds % 60:02}", True, 'white')

	def updateRect(self, coordinates):
		self.__rect.move(coordinates[0], coordinates[1])

	def getRectCoordinates(self):
		return self.__rect.x, self.__rect.y


class Score:
	def __init__(self, coordinates):
		self.__score = 0
		self.font = pg.font.Font(os.path.join(os.path.dirname(__file__), '../assets\\Helvetica-Font\\Helvetica.ttf'), 24)
		self.text = self.font.render(f'Score: {self.__score}', True, 'white')
		self.__rect = self.text.get_rect(topleft=coordinates)

	def getScore(self):
		return self.__score

	def updateScore(self, score):
		self.__score += score

	def updateRect(self, coordinates):
		self.__rect.move(coordinates[0], coordinates[1])

	def getRectCoordinates(self):
		return self.__rect.x, self.__rect.y

	def unknown(self):
		pass


class Text:  # Turn this into square, and alter it so if a tile is passed in then that gets put in I guess, smth like that
	def __init__(self, coordinates, size, text):
		self.font = pg.font.Font(os.path.join(os.path.dirname(__file__), '../assets\\Helvetica-Font\\Helvetica.ttf'), 14)
		self.text = self.font.render(f'{text}', True, 'white')
		self.rect = pg.Rect(coordinates, size)

	def updateText(self, text):
		self.text = self.font.render(f'{text}', True, 'white')


class Square:
	def __init__(self, coordinates, text=' '):
		self.__font = pg.font.Font(os.path.join(os.path.dirname(__file__), '../assets\\Helvetica-Font\\Helvetica.ttf'), 16)
		self.__text = self.__font.render(f'{text}', True, 'white')
		self.__rect = self.__text.get_rect()
		self.__rect.update(coordinates[0], coordinates[1], 32, 32)
		self.squareType = text

	def getRectCoordinates(self):
		return self.__rect.x, self.__rect.y

	def getSquareRect(self):
		return self.__rect

	def getText(self):
		return self.__text

	def getType(self):
		return self.squareType


'''
1. removed from sprites list for rack
2. removed from contents of rack
3. square scanned for specialLocation (which is extracted)
4. tile letter enters square
5. tile Rect updated to Square Rect
6. tile image resized
7. tile sprite replaces Square in board.squares
8. tile added to board group
9. tile sprite is in board.squares, but because it isn't a Square object it's ignored when blitting the Squares

Steps to undo a move:
1. remove tile from board group
2. replace tile sprite with Square (need to access row & column, rect of tile, and use specialLocation to create Square)
3. update tile rect back to original position (can calculate with rackPosition)
4. resize tile image back to OG size (go find what this is, i think it's 48x48 but i can't remember)
5. replace tile letter with specialLocation
6. add tile letter into rack contents
7. add tile sprite back to sprites list for rack
8. repeat for each tile placed

Note: bc you need row & column, put that into stack. DO NOT FORGET THIS.
'''

