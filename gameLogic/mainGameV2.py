import pygame as pg
import pygame_gui as py_gui
from gameLogic import ScrabbleItemTemplates
from gameLogic.ScrabbleItemTemplates import EnglishLetters, FrenchLetters, SpanishLetters
import os
import random

'''Game Logic Area'''

gameBoard = None
Player1 = None
Player2 = None
TileBag = None


def initialiseEverything(language):
	global gameBoard, Player1, Player2, TileBag
	gameBoard = ScrabbleItemTemplates.Board((400, 10))
	Player1 = ScrabbleItemTemplates.Player((550, 775))
	Player2 = ScrabbleItemTemplates.Player((550, 775))
	TileBag = ScrabbleItemTemplates.TileBag((50, 250), language)

	startGameWindow()


def startGameWindow():
	pg.init()

	pg.display.set_caption('Scrabble Tournament Game')
	gameWindow = pg.display.set_mode((1600, 900))

	background = pg.Surface((1600, 900))
	background.fill(pg.Color('#654264'))

	UIManager = py_gui.UIManager((1600, 900))
	clock = pg.time.Clock()

	fillRack_button = py_gui.elements.UIButton(relative_rect=pg.Rect((84, 650), (100, 50)), text='Fill Rack', manager=UIManager)
	shuffleBag_button = py_gui.elements.UIButton(relative_rect=pg.Rect((218, 650), (100, 50)), text='Shuffle', manager=UIManager)

	running = True
	Player1_Turn = True
	while running:
		time_delta = clock.tick(30) / 1000.0
		for event in pg.event.get():

			if event.type == pg.QUIT:
				running = False

			if event.type == py_gui.UI_BUTTON_PRESSED:
				if event.ui_element == fillRack_button:
					Player1.rack.fillRack(TileBag)
				if event.ui_element == shuffleBag_button:
					TileBag.shuffleBag()

			UIManager.process_events(event)

		UIManager.update(time_delta)
		gameWindow.blit(background, (0, 0))
		UIManager.draw_ui(gameWindow)

		gameWindow.blit(gameBoard.image.convert_alpha(), (gameBoard.rect.x, gameBoard.rect.y))
		gameWindow.blit(TileBag.image.convert_alpha(), (TileBag.rect.x, TileBag.rect.y))

		if Player1_Turn:
			gameWindow.blit(Player1.rack.image.convert_alpha(), (Player1.rack.rect.x, Player1.rack.rect.y))
			Player1.rack.group.draw(gameWindow)
		else:
			gameWindow.blit(Player2.rack.image.convert_alpha(), (Player2.rack.rect.x, Player2.rack.rect.y))
			Player2.rack.group.draw(gameWindow)

		pg.display.update()

	pg.quit()
	print('okay game is closed')
