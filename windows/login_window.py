import pygame as pg
from windowsTemplate import *

def launch_homescreen_window():
	homescreenWindow = Window((1280, 720), 'Scrabble Training Tool')
	homescreenWindow.launch_window()

	clock = pg.time.Clock()

	running = True
	while running:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False

		homescreenWindow.wipe()

		homescreenWindow.update_display()
		clock.tick(60)

	homescreenWindow.kill()

launch_homescreen_window()