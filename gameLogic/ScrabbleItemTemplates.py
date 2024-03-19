import pygame as pg
import os
import random

AllScrabbleLetters = [' ', 'A', 'B', 'C', 'CH', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'LL', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'RR', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

EnglishQuantities = [2, 9, 2, 2, None, 4, 12, 2, 3, 2, 9, 1, 1, 4, None, 2, 6, None, 8, 2, 1, 6, None, 4, 6, 4, 2, 2, 1, 2, 1]
EnglishScore = [0, 1, 3, 3, None, 2, 1, 4, 2, 4, 1, 8, 5, 1, None, 3, 1, None, 1, 3, 10, 1, None, 1, 1, 1, 4, 4, 8, 4, 10]
EnglishLetters = {letter: (score, quantity) for letter, score, quantity in zip(AllScrabbleLetters, EnglishScore, EnglishQuantities) if (score is not None and quantity is not None)}

FrenchQuantities = [0, 9, 2, 2, None, 3, 15, 2, 2, 2, 8, 1, 1, 5, None, 3, 6, None, 6, 2, 1, 6, None, 6, 6, 6, 2, 1, 1, 1, 1]
FrenchScore = [0, 1, 3, 3, None, 2, 1, 4, 2, 4, 1, 8, 10, 1, None, 2, 1, None, 1, 3, 8, 1, None, 1, 1, 1, 4, 10, 10, 10, 10]
FrenchLetters = {letter: (score, quantity) for letter, score, quantity in zip(AllScrabbleLetters, FrenchScore, FrenchQuantities) if (score is not None and quantity is not None)}

SpanishQuantities = [2, 12, 2, 4, 1, 5, 12, 1, 2, 2, 6, 1, None, 4, 1, 2, 5, 1, 9, 2, 1, 5, 1, 6, 4, 5, 1, None, 1, 1, 1]
SpanishScore = [0, 1, 3, 3, 5, 2, 1, 4, 2, 4, 1, 8, None, 1, 8, 3, 1, 8, 1, 3, 5, 1, 8, 1, 1, 1, 4, None, 8, 4, 10]
SpanishLetters = {letter: (score, quantity) for letter, score, quantity in zip(AllScrabbleLetters, SpanishScore, SpanishQuantities) if (score is not None and quantity is not None)}

REGULAR_TIME = 1500 # 25 minutes / 1500 seconds
OVERTIME_TIME = 600 # 10 minutes / 600 seconds


class Tile(pg.sprite.Sprite):
	def __init__(self, filename, coordinates, letter, score):
		super().__init__()
		self.image = pg.image.load(os.path.join(os.path.dirname(__file__), f'../assets\\images\\{filename}'))
		self.coordinates = coordinates
		self.letter = letter
		self.score = score
		self.rect = self.image.get_rect().move(coordinates[0], coordinates[1])

	def updateCoordinates(self, coordinates):
		self.coordinates = coordinates

	def updateRect(self, coordinates):
		self.rect = self.rect.move(coordinates[0], coordinates[1])

	def transformImage(self, size):
		self.image = pg.transform.scale(self.image, size)

	def getScore(self):
		return self.score

	def getLetter(self):
		return self.letter

	def getRect(self):
		return self.rect.x, self.rect.y

	def getCoordinates(self):
		return self.coordinates


class Board(pg.sprite.Sprite):
	def __init__(self, coordinates):
		super().__init__()
		self.board = [['' for i in range(15)] for j in range(15)]
		self.image = pg.image.load(os.path.join(os.path.dirname(__file__), '../assets\\images\\GameBoard.png'))
		self.rect = self.image.get_rect(topleft=coordinates)
		self.group = pg.sprite.Group()
		self.SpecialLocations = {
			'TW': [(0, 0), (0, 7), (0, 14), (7, 0), (14, 0), (14, 7), (14, 14)],
			'DW': [(1, 1), (2, 2), (3, 3), (4, 4), (4, 10), (3, 11), (2, 12), (1, 13)],
			'TL': [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 13)],
			'DL': [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (6, 6), (6, 8), (6, 12), (7, 3), (7, 11), (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)]
		}
		self.addSpecialLocations()

	def addToGroup(self, sprite):
		self.group.add(sprite)

	def addToBoard(self, position, letter):
		self.board[position[0]][position[1]] = letter

	def addSpecialLocations(self):
		for bonusType in self.SpecialLocations.keys():
			for position in self.SpecialLocations[bonusType]:
				self.board[position[0]][position[1]] = bonusType

	def getBoard(self):
		return self.board

	def transformBoard(self, size):
		self.image = pg.transform.scale(self.image, size)

	def checkSpecialLocation(self, position):
		if self.board[position[0]][position[1]] in self.SpecialLocations.keys():
			return self.board[position[0]][position[1]]
		else:
			return ''

	def unknown(self):
		pass


class Rack(pg.sprite.Sprite):
	def __init__(self, coordinates, rackType):
		super().__init__()
		self.image = pg.image.load(
			os.path.join(os.path.dirname(__file__), f'../assets\\images\\Deck{rackType}.png'))
		self.rect = self.image.get_rect(topleft=coordinates)
		self.size = 7
		self.contents = ['' for i in range(7)]
		self.group = pg.sprite.Group()

	def fillRack(self, tileBag):
		while '' in self.contents and not tileBag.empty:
			letters = tileBag.bag[:-1]
			letter = random.choice(letters)
			indexPosition = tileBag.bag.index(letter)
			if tileBag.bag[indexPosition][2] > 0:
				self.contents[self.contents.index('')] = letter[0]
				tileBag.bag[indexPosition] = (letter[0], letter[1], (letter[2]-1))
				if letter[2] - 1 == 0:
					tileBag.bag[-1] += 1
		self.fillRackGroup(tileBag.language, tileBag)

	def fillRackGroup(self, language, tileBag):
		self.group.empty()
		lettersToDraw = ['' for i in range(7)]
		for idxPosition, letterToFind in enumerate(tileBag.bag[:-1]):
			for indexPosition, letterTaken in enumerate(self.contents):
				if letterToFind[0] == letterTaken:
					lettersToDraw[indexPosition] = idxPosition

		for i, letterToDraw in enumerate(lettersToDraw):
			filename = f'{language}Letters\\TILE_{tileBag.bag[letterToDraw][0]}.png'
			coordinates = (584+i*64, 798)
			letter = tileBag.bag[letterToDraw][0]
			score = tileBag.bag[letterToDraw][1]
			self.group.add(Tile(filename, coordinates, letter, score))

	def pickTile(self, language, tileBag):
		item = random.choice(tileBag.bag[:-1])
		indexPosition = tileBag.bag.index(item)
		letter = tileBag.bag[indexPosition][0]
		return letter

	def updateImage(self, rackType):
		self.image = pg.image.load(
			os.path.join(os.path.dirname(__file__), f'../assets\\images\\Deck{rackType}.png'))

	def updateRect(self, coordinates):
		self.rect = self.rect.move(coordinates[0], coordinates[1])

def fillBag(lexicon):
	tile_bag = []
	for letter in lexicon.keys():
		tile_bag.append((letter, lexicon[letter][0], lexicon[letter][1]))
	tile_bag.append(0)
	return tile_bag


class TileBag(pg.sprite.Sprite):
	def __init__(self, coordinates, language):
		super().__init__()
		self.image = pg.image.load(os.path.join(os.path.dirname(__file__), f'../assets\\images\\TileBag.png'))
		self.rect = self.image.get_rect(topleft=coordinates)
		self.bag = []
		self.language = language
		self.empty = False
		self.shuffleCount = 0

		match self.language:
			case 'English':
				self.bag = fillBag(EnglishLetters)
				self.alphabet = list(EnglishLetters.keys())
			case 'French':
				self.bag = fillBag(FrenchLetters)
				self.alphabet = list(FrenchLetters.keys())
			case 'Spanish':
				self.bag = fillBag(SpanishLetters)
				self.alphabet = list(SpanishLetters.keys())
			case _:
				self.bag = fillBag(EnglishLetters)
				self.alphabet = list(EnglishLetters.keys())

	def shuffleBag(self):
		if self.shuffleCount < 2:
			lettersInBag = self.bag[:-1]
			emptyLetters = self.bag[-1]
			random.shuffle(lettersInBag)
			self.bag = lettersInBag
			self.bag.append(emptyLetters)
			self.shuffleCount += 1

	def isEmpty(self):
		if self.bag[-1] == len(self.bag) - 1:
			self.empty = True


class Player:
	def __init__(self, coordinates, rackType):
		self.rack = Rack(coordinates, rackType)
		self.score = None
		self.penalties = 0
		self.timer = None

	def getScore(self):
		return self.score

	def updateScore(self, scoreToAdd):
		self.score += scoreToAdd


class Timer:
	def __init__(self, initialSeconds, coordinates):
		self.font = pg.font.Font(os.path.join(os.path.dirname(__file__), '../assets\\Helvetica-Font\\Helvetica.ttf'), 24)
		self.current_seconds = initialSeconds
		self.text = self.font.render(f"Time Left: {self.current_seconds // 60:02}:{self.current_seconds % 60:02}", True, 'white')
		self.rect = self.text.get_rect(topleft=coordinates)

	def updateTimer(self):
		self.text = self.font.render(f"Time Left: {self.current_seconds // 60:02}:{self.current_seconds % 60:02}", True, 'white')


class Score:
	def __init__(self, coordinates):
		self.score = 0
		self.font = pg.font.Font(os.path.join(os.path.dirname(__file__), '../assets\\Helvetica-Font\\Helvetica.ttf'),
								 24)
		self.text = self.font.render(f'Score: {self.score}', True, 'white')
		self.rect = self.text.get_rect(topleft=coordinates)


class Button:
	pass
