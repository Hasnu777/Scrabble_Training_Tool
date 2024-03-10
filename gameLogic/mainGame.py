import pygame as pg
import pygame_gui as py_gui
from gameLogic import ScrabbleItemTemplates
from gameLogic.ScrabbleItemTemplates import EnglishLetters, FrenchLetters, SpanishLetters
import sys
import os

'''Game Logic Area'''


def createBoard():
	board = [[] for i in range(15)]
	boardImage = pg.image.load(
		os.path.join(os.path.dirname(__file__), '../assets\\images\\GameBoard.png'))
	boardImage = pg.transform.scale(boardImage, (700, 700))
	boardGroup = pg.sprite.Group()
	return board, boardImage, boardGroup


def createPlayer1Deck():
	player1_Deck = []
	player1_DeckImage = pg.image.load(
		os.path.join(os.path.dirname(__file__), '../assets\\images\\DeckFront.png'))
	player1_DeckGroup = pg.sprite.Group()
	return player1_Deck, player1_DeckImage, player1_DeckGroup


def createPlayer2Deck():
	player2_Deck = []
	player2_DeckImage = pg.image.load(
		os.path.join(os.path.dirname(__file__), '../assets\\images\\DeckBack.png'))
	player2_DeckGroup = pg.sprite.Group()
	return player2_Deck, player2_DeckImage, player2_DeckGroup


def fillTileBag(lexicon):
	tile_bag = []
	for letter in lexicon.keys():
		tile_bag.append((ScrabbleItemTemplates.Tile('UserProfileIcon', (0, 0), letter, score=lexicon[letter][0]), lexicon[letter][1]))
	return tile_bag


def initialiseTileBag(lang):
	match lang:
		case 'English':
			tile_bag = fillTileBag(EnglishLetters)
		case 'French':
			tile_bag = fillTileBag(FrenchLetters)
		case 'Spanish':
			tile_bag = fillTileBag(SpanishLetters)
		case _:
			tile_bag = fillTileBag(EnglishLetters)
	tile_bagImage = pg.image.load(os.path.join(os.path.dirname(__file__), '../assets\\images\\TileBag.png'))
	return tile_bag, tile_bagImage


def initialiseEverything():
	global gameBoard, gameBoardImage, gameBoardGroup
	gameBoard, gameBoardImage, gameBoardGroup = createBoard()

	global Player1_Deck, Player1_DeckImage, Player1_DeckGroup
	Player1_Deck, Player1_DeckImage, Player1_DeckGroup = createPlayer1Deck()

	global Player2_Deck, Player2_DeckImage, Player2_DeckGroup
	Player2_Deck, Player2_DeckImage, Player2_DeckGroup = createPlayer2Deck()

	global tileBag, tileBagImage
	tileBag, tileBagImage = initialiseTileBag('English')

	startGameWindow()


'''PyGame Area'''


def startGameWindow():
	pg.init()

	pg.display.set_caption('Scrabble Tournament Game')
	gameWindow = pg.display.set_mode((1600, 900))

	background = pg.Surface((1600, 900))
	background.fill(pg.Color('#654264'))

	UIManager = py_gui.UIManager((1600, 900))
	clock = pg.time.Clock()

	hello_button = py_gui.elements.UIButton(relative_rect=pg.Rect((350, 275), (100, 50)), text='Say Hi', manager=UIManager)

	running = True
	while running:
		time_delta = clock.tick(30) / 1000.0
		for event in pg.event.get():

			if event.type == pg.QUIT:
				running = False

			UIManager.process_events(event)

		UIManager.update(time_delta)
		gameWindow.blit(background, (0, 0))
		UIManager.draw_ui(gameWindow)

		gameWindow.blit(gameBoardImage.convert_alpha(), (475, 87))
		gameWindow.blit(tileBagImage.convert_alpha(), (100, 250))
		gameWindow.blit(Player1_DeckImage.convert_alpha(), (550, 775))
		gameWindow.blit(Player2_DeckImage.convert_alpha(), (550, 25))

		pg.display.update()

	pg.quit()
	print('okay game is closed')
