import pygame as pg
import pygame_gui as pgui
import ScrabbleItemTemplates
import os
from ScrabbleItemTemplates import EnglishLetters, FrenchLetters, SpanishLetters

print(EnglishLetters)
print(FrenchLetters)
print(SpanishLetters)

'''PyGame + PyGUI core'''
pg.init()

pg.display.set_caption('AI Scrabble Trainer')
gameSurface = pg.display.set_mode((1600, 900))

background = pg.Surface((1600, 900))
background.fill(pg.Color('#378521'))

manager = pgui.UIManager((1600, 900))

# hello_button = pgui.elements.UIButton(relative_rect=pg.Rect((350, 275), (100, 50)), text='Say Hi', manager=manager)

clock = pg.time.Clock()
running = True


'''Scrabble related things'''

# Creating tile bag
language = 'English'  # will be variable taken in from the tkinter window

if language == 'English':
	tileBag = ScrabbleItemTemplates.Bag(size=100, coordinates=(0, 0))
	for letter in EnglishLetters.keys():
		for quantity in EnglishLetters[letter][0]:
			tileBag.bag.append(
				ScrabbleItemTemplates.Tile(coordinates=(0, 0), letter=letter, score=EnglishLetters[letter][1]))
			tileBag.group.append(tileBag.bag[-1])

if language == 'French':
	tileBag = ScrabbleItemTemplates.Bag(size=102, coordinates=(0, 0))
	for letter in FrenchLetters.keys():
		for quantity in FrenchLetters[letter][0]:
			tileBag.bag.append(
				ScrabbleItemTemplates.Tile(coordinates=(0, 0), letter=letter, score=FrenchLetters[letter][1]))

if language == 'Spanish':
	tileBag = ScrabbleItemTemplates.Bag(size=100, coordinates=(0, 0))
	for letter in SpanishLetters.keys():
		for quantity in SpanishLetters[letter][0]:
			tileBag.bag.append(
				ScrabbleItemTemplates.Tile(coordinates=(0, 0), letter=letter, score=SpanishLetters[letter][1]))

# Creating board
board = pg.image.load(os.path.join(__file__, '../assets\\images\\GameBoard.png'))
board = pg.transform.scale(board, (600, 600))
boardGroup = pg.sprite.Group()

boardGroupSingle = pg.sprite.GroupSingle()
boardGroupSingle.add(board)


while running:
	time_delta = clock.tick(30)/1000.0
	for event in pg.event.get():

		if event.type == pg.QUIT:
			running = False

		# if event.type == pgui.UI_BUTTON_PRESSED:
		# 	if event.ui_element == hello_button:
		# 		print('Whassup')

		manager.process_events(event)

	manager.update(time_delta)
	gameSurface.draw(boardGroupSingle)
	gameSurface.blit(background, (0, 0))
	manager.draw_ui(gameSurface)
	pg.display.update()

pg.quit()
