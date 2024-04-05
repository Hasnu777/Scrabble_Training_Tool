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
	Player1 = ScrabbleItemTemplates.Player((550, 775), 'Front')
	Player2 = ScrabbleItemTemplates.Player((550, 775), 'Back')
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

	fillRack_button = py_gui.elements.UIButton(relative_rect=pg.Rect((84, 650), (100, 50)), text='Fill Rack', manager=UIManager)  # Need to mention ui_button has been edited in the NEA doc
	fillRack_button.disable()

	shuffleBag_button = py_gui.elements.UIButton(relative_rect=pg.Rect((218, 650), (100, 50)), text='Shuffle', manager=UIManager)  # Commented some code in the UIButton class to prevent pygame.USEREVENT usage
	shuffleBag_button.disable()

	determineOrder_button = py_gui.elements.UIButton(relative_rect=pg.Rect((84, 725), (100, 50)), text='Pick Tile', manager=UIManager)

	swapTurn_button = py_gui.elements.UIButton(relative_rect=pg.Rect((218, 725), (100, 50)), text='Swap', manager=UIManager)
	swapTurn_button.disable()

	global Player1
	Player1.timer = ScrabbleItemTemplates.Timer(ScrabbleItemTemplates.REGULAR_TIME, (1180, 750))
	Player1.score = ScrabbleItemTemplates.Score((1180, 720))

	global Player2
	Player2.timer = ScrabbleItemTemplates.Timer(ScrabbleItemTemplates.REGULAR_TIME, (1180, 75))
	Player2.score = ScrabbleItemTemplates.Score((1180, 45))

	pg.time.set_timer(pg.USEREVENT, 1000)

	running = True
	Player1_Turn = True
	orderDetermined = False
	readyToStart = False

	while running:

		time_delta = clock.tick(30) / 1000.0

		# If players have picked a tile and determined the order, determineOrder_button is killed & shuffleBag_Button is enabled
		if orderDetermined:
			determineOrder_button.kill()
			shuffleBag_button.enable()

		# If the tile bag has been shuffled, the shuffleBag_button is removed, and fillRack_button & swapTurn_button is enabled
		if TileBag.shuffleCount >= 2:
			shuffleBag_button.kill()
			fillRack_button.enable()
			swapTurn_button.enable()

		# Going through all events that occur during each tick
		for event in pg.event.get():

			if event.type == pg.QUIT:
				running = False
				break

			# if a pygame_gui button has been pressed
			if event.type == py_gui.UI_BUTTON_PRESSED:

				# if fillRack_button has been pressed
				if event.ui_element == fillRack_button:
					Player1.rack.fillRack(TileBag)
					Player2.rack.fillRack(TileBag)
					readyToStart = True

				# if shuffleBag_button has been pressed
				if event.ui_element == shuffleBag_button:
					TileBag.shuffleBag()

				# if swapTurn_button has been pressed
				if event.ui_element == swapTurn_button:
					Player1_Turn = not Player1_Turn

				# If determineOrder_button has been pressed
				if event.ui_element == determineOrder_button:
					tile1 = ''
					tile2 = ''

					# Picks a random tile, while loop used to ensure the same tile isn't picked.
					# TODO: check what occurs if the same tile is picked in an actual scrabble game
					while tile1 == tile2:
						tile1 = Player1.rack.pickTile(TileBag)
						tile2 = Player2.rack.pickTile(TileBag)

					# If Player1's tile is higher in the alphabet than Player2's tile
					if TileBag.alphabet.index(tile1) < TileBag.alphabet.index(tile2):
						print(f'no swap occurred: {tile1} v {tile2}')

					# If Player2's tile is higher in the alphabet than Player2's tile, Player1 and Player2 swap
					else:
						Player1.rack.image, Player2.rack.image = Player2.rack.image, Player1.rack.image
						Player1.rack.rect, Player2.rack.rect = Player2.rack.rect, Player1.rack.rect
						Player1.score, Player2.score = Player2.score, Player1.score
						Player1.timer, Player2.timer = Player2.timer, Player1.timer
						Player1, Player2 = Player2, Player1
						print(f'swap occurred: {tile1} v {tile2}')
					orderDetermined = True

			# Used to decrement the timer
			if event.type == pg.USEREVENT and readyToStart:
				if Player1.timer.current_seconds != 0 and Player1_Turn:
					Player1.timer.current_seconds -= 1
					Player1.timer.updateTimer()

				if Player2.timer.current_seconds != 0 and not Player1_Turn:
					Player2.timer.current_seconds -= 1
					Player2.timer.updateTimer()

			if event.type == pg.MOUSEBUTTONDOWN:

				mouse_pos = pg.mouse.get_pos()
				print(mouse_pos)
				if Player1_Turn:
					for i, tile in enumerate(Player1.rack.sprites.values()):
						if tile is not None:
							if tile.rect.collidepoint(mouse_pos):
								tile.is_clicked = True
								Player1.rack.contents[i] = ''
								print(i, end=' ')
								Player1.rack.sprites[f'TILE{i+1}'].getLetter()
								Player1.rack.sprites[f'TILE{i + 1}'] = None
								continue
							print(i, end=' ')
							Player1.rack.sprites[f'TILE{i+1}'].getLetter()
				else:
					for i, tile in enumerate(Player2.rack.sprites.values()):
						if tile is not None:
							if tile.rect.collidepoint(mouse_pos):
								tile.is_clicked = True
								Player2.rack.sprites[f'TILE{i + 1}'] = None

			if event.type == pg.MOUSEBUTTONUP:

				mouse_pos = pg.mouse.get_pos()

				if Player1_Turn:
					for tile in Player1.rack.sprites.values():
						if tile is not None:
							if tile.is_clicked:
								tile.rect.move(mouse_pos[0], mouse_pos[1])
								tile.coordinates = mouse_pos
								tile.is_clicked = False
				else:
					for tile in Player2.rack.sprites.values():
						if tile is not None:
							if tile.is_clicked:
								tile.rect.move(mouse_pos[0], mouse_pos[1])
								tile.coordinates = mouse_pos
								tile.is_clicked = False

			# Processing anything pygame_gui related for the event
			UIManager.process_events(event)

		# Update game window, draw background, and draw buttons
		UIManager.update(time_delta)
		gameWindow.blit(background, (0, 0))
		UIManager.draw_ui(gameWindow)

		# Blit the board and tile bag
		gameWindow.blit(gameBoard.image.convert_alpha(), (gameBoard.rect.x, gameBoard.rect.y))
		gameWindow.blit(TileBag.image.convert_alpha(), (TileBag.rect.x, TileBag.rect.y))

		# Blit the rack and tiles for whose turn it is
		if Player1_Turn:
			gameWindow.blit(Player1.rack.image.convert_alpha(), (Player1.rack.rect.x, Player1.rack.rect.y))
			Player1.rack.group.draw(gameWindow)
		else:
			gameWindow.blit(Player2.rack.image.convert_alpha(), (Player2.rack.rect.x, Player2.rack.rect.y))
			Player2.rack.group.draw(gameWindow)

		# Blit the score and timer for both players
		gameWindow.blit(Player1.timer.text, Player1.timer.rect)
		gameWindow.blit(Player1.score.text, Player1.score.rect)

		gameWindow.blit(Player2.timer.text, Player2.timer.rect)
		gameWindow.blit(Player2.score.text, Player2.score.rect)

		pg.display.update()

	pg.quit()
	print('okay game is closed')
