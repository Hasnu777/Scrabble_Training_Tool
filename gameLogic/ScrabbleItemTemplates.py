# import pygame as pg
# # import pygame_gui as pgui
# import os
# import random
#
# # Constants
# # scrabbleLetters = ["A", "B", "C", "D", "E", "F", "U", "V", "W", "X", "Y", "Z", " ", "LL", "CH", "RR", ]
# # EnglishQuantityInBag = [9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6, 8, 2, 1, 6, 4, 6, 4, 2, 2, 1, 2, 1, 2]
# # EnglishScores = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 4, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10, 0]
# # EnglishLetters = {letter:quantity for letter, quantity in zip(scrabbleLetters, alphabetQuantityInBag)}
# # letterPoints = {letter:point for letter, point in zip(scrabbleLetters, points)}
#
#
# AllScrabbleLetters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
# 					  "T", "U", "V", "W", "X", "Y", "Z", " ", "CH", "LL", "Ñ", "RR"]
# EnglishLetterQuantities = [9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6, 8, 2, 1, 6, 4, 6, 4, 2, 2, 1, 2, 1, 2, None, None, None, None]
# EnglishLetterScores = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 4, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10, 0, None, None, None, None]
# EnglishLetters = {letter: (quantity, score) for letter, quantity, score in zip(AllScrabbleLetters, EnglishLetterQuantities, EnglishLetterScores) if None not in (letter, score)}
#
# FrenchLetterQuantities = [9, 2, 2, 3, 15, 2, 2, 2, 8, 1, 1, 5, 3, 6, 6, 2, 1, 6, 6, 6, 6, 2, 1, 1, 1, 1, 2, None, None, None, None]
# FrenchLetterScores = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 10, 1, 2, 1, 1, 3, 1, 1, 1, 1, 4, 10, 10, 10, 10, 0, None, None, None, None]
# FrenchLetters = {letter: (quantity, score) for letter, quantity, score in zip(AllScrabbleLetters, FrenchLetterQuantities, FrenchLetterScores) if None not in (letter, score)}
#
# SpanishLetterQuantities = [12, 2, 4, 5, 12, 1, 2, 2, 6, 1, None, 4, 2, 5, 9, 2, 1, 5, 6, 4, 5, 1, None, 1, 1, 1, 2, 1, 1, 1, 1]
# SpanishLetterScores = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, None, 1, 3, 1, 1, 3, 1, 1, 1, 1, 4, None, 8, 4, 10, 0, 5, 8, 8, 8,]
# SpanishLetters = {letter: (quantity, score) for letter, quantity, score in zip(AllScrabbleLetters, SpanishLetterQuantities, SpanishLetterScores) if None not in (letter, score)}
# # Spanish: no K, no W. Has LL, ~N, RR, CH
# # ERRORS PRESENT IN CREATION OF THE LAST VARIABLE OF EACH GROUP. PLEASE CHECK AND FIX THESE ERRORS. issue pic in assets
#
#
# class Tile(pg.sprite.Sprite):
# 	def __init__(self, coordinates, letter, score, filename='UserProfileIcon'):
# 		super().__init__()
# 		self.image = pg.image.load(
# 			os.path.join(os.path.dirname(__file__), f'../assets\\images\\{filename}.png')).convert_alpha()
# 		self.rect = self.image.get_rect(midbottom=coordinates)
# 		self.letter = letter
# 		self.score = score
#
# 	def getLetter(self):
# 		return self.letter
#
# 	def getScore(self):
# 		return self.score
#
# # Will need to add more here
#
#
# class Bag(pg.sprite.Sprite):
# 	def __init__(self, size, coordinates, filename='SettingsIcon'):
# 		super().__init__()
# 		self.image = pg.image.load(
# 			os.path.join(os.path.dirname(__file__), f'../assets\\images\\{filename}.png')).convert_alpha()
# 		self.rect = self.image.get_rect(midbottom=coordinates)
# 		self.size = size
# 		self.bag = []
# 		self.group = pg.sprite.Group()
#
# 	def shuffle(self):
# 		random.shuffle(self.bag)
#
# 	def removeTile(self):
# 		return self.bag.pop(self.bag[random.randint(0, len(self.bag)) - 1])  # should be fine
#
# 	def addTile(self, tile):
# 		self.bag.append(tile)
#
# 	def peekAtTiles(self):
# 		return [tile.letter for tile in self.bag]  # this prob needs to change, fine for now though
#
#
# class Rack(pg.sprite.Sprite):
# 	def __init__(self, coordinates, filename='LoadGameIcon'):
# 		super().__init__()
# 		self.image = pg.image.load(
# 			os.path.join(os.path.dirname(__file__), f'../assets\\images\\{filename}.png')).convert_alpha()
# 		self.rect = self.image.get_rect(midbottom=coordinates)
# 		self.size = 7
# 		self.contents = []
# 		self.group = pg.sprite.Group()
#
# 	def removeFromRack(self):
# 		return None  # need to figure out how this removal crap works first


import pygame as pg
import os

AllScrabbleLetters = [' ', 'A', 'B', 'C', 'CH', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'LL', 'M', 'N', 'Ñ' 'O',
					  'P', 'Q', 'R', 'RR' 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

EnglishQuantities = [2, 9, 2, 2, None, 4, 12, 2, 3, 2, 9, 1, 1, 4, None, 2, 6, None, 8, 2, 1, 6, None, 4, 6, 4, 2, 2, 1,
					 2, 1]
EnglishScore = [0, 1, 3, 3, None, 2, 1, 4, 2, 4, 1, 8, 5, 1, None, 3, 1, None, 1, 3, 10, 1, None, 1, 1, 1, 4, 4, 8, 4,
				10]
EnglishLetters = {letter: (score, quantity) for letter, score, quantity in
				  zip(AllScrabbleLetters, EnglishScore, EnglishQuantities) if score is not None}

FrenchQuantities = [0, 9, 2, 2, None, 3, 15, 2, 2, 2, 8, 1, 1, 5, None, 3, 6, None, 6, 2, 1, 6, None, 6, 6, 6, 2, 1, 1,
					1, 1]
FrenchScore = [0, 1, 3, 3, None, 2, 1, 4, 2, 4, 1, 8, 10, 1, None, 2, 1, None, 1, 3, 8, 1, None, 1, 1, 1, 4, 10, 10, 10,
			   10]
FrenchLetters = {letter: (score, quantity) for letter, score, quantity in
				 zip(AllScrabbleLetters, FrenchScore, FrenchQuantities) if score is not None}

SpanishQuantities = [2, 12, 2, 4, 1, 5, 12, 1, 2, 2, 6, 1, None, 4, 1, 2, 5, 1, 9, 2, 1, 5, 1, 6, 4, 5, 1, None, 1, 1,
					 1]
SpanishScore = [0, 1, 3, 3, 5, 2, 1, 4, 2, 4, 1, 8, None, 1, 8, 3, 1, 8, 1, 3, 5, 1, 8, 1, 1, 1, 4, None, 8, 4, 10]
SpanishLetters = {letter: (score, quantity) for letter, score, quantity in
				  zip(AllScrabbleLetters, SpanishScore, SpanishQuantities) if score is not None}


class Tile(pg.sprite.Sprite):
	def __init__(self, filename, coordinates, letter, score):
		super().__init__()
		self.image = pg.image.load(os.path.join(os.path.dirname(__file__), f'../assets\\images\\{filename}.png'))
		self.coordinates = coordinates
		self.letter = letter
		self.score = score
