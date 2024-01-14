# import pygame as pg
# import tkinter as tk
# import pygame_gui as pygui
# class Window():
#
# 	def __init__(self, resolution, windowTitle, backgroundImage=None, iconImage=None):
# 		self.resolution = resolution
# 		self.title = windowTitle
# 		self.backgroundImage = backgroundImage
# 		self.iconImage = iconImage
# 		self.screen = None
# 		self.components = []
#
# 	def launch_window(self):
# 		pg.init()
# 		self.screen = pg.display.set_mode(self.resolution, pg.RESIZABLE, vsync=1)
# 		pg.display.set_caption(self.title)
#
# 	def update_display(self):
# 		pg.display.flip()
#
# 	def wipe(self):
# 		self.screen.fill((0,0,0))
#
# 	def kill(self):
# 		pg.quit()
#
# 	def add_component(self, component):
# 		self.components.append(component)
#
# 	def remove_component(self, component):
# 		self.components.remove(component)
#
#
# class Button():
# 	def __init__(self, window, xpos, ypos, width, height, text, action):
# 		self.window = window
# 		self.xpos = xpos
# 		self.ypos = ypos
# 		self.width = width
# 		self.height = height
# 		self.text = text
# 		self.action = action
# 		self.image = pg.Surface((width, height))
# 		self.image.fill((255,255,255))
# 		pg.font.init()
# 		self.font = pg.font.SysFont('Courier', 36)
# 		self.text_surface = self.font.render(text, True, (0,0,0))
# 		self.rect = self.image.get_rect(center=(xpos + width / 2, ypos + height / 2))
#
# 	def handle_events(self, event):
# 		if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
# 			self.action()
#
# 	def handle_updates(self):
# 		pass
#
# 	def handle_draws(self):
# 		self.image.blit(self.text_surface, (self.width / 2 - self.text_surface.get_width() / 2, self.height / 2 - self.text_surface.get_height() / 2))
# 		self.window.screen.blit(self.image, self.rect)
#
# def launch_test_window():
# 	testWindow = Window((800, 600), 'Test Window')
# 	testButton1 = Button(testWindow, 100, 100, 250, 50, 'Click me you bum', lambda: print('deez nuts'))
# 	testButton2 = Button(testWindow, 500, 500, 200, 50, 'commit murder', testWindow.kill)
# 	testWindow.add_component(testButton1)
# 	testWindow.add_component(testButton2)
# 	print('launching now...')
# 	testWindow.launch_window()
# 	print('window dead')
#
# launch_test_window()

import pygame as pg
import pygame_gui as pygui


class Window():

	def __init__(self, resolution, windowTitle, backgroundImage=None, iconImage=None):
		self.resolution = resolution
		self.title = windowTitle
		self.backgroundImage = backgroundImage
		self.iconImage = iconImage
		self.screen = None
		self.components = []

	def launch_window(self):
		pg.init()
		self.screen = pg.display.set_mode(self.resolution, pg.RESIZABLE, vsync=1)
		pg.display.set_caption(self.title)

	def update_display(self):
		pg.display.flip()

	def wipe(self):
		self.screen.fill((0, 0, 0))

	def kill(self):
		pg.quit()

	def add_component(self, component):
		self.components.append(component)

	def remove_component(self, component):
		self.components.remove(component)


class Button:
	def __init__(self, window, xpos, ypos, width, height, text, action):
		self.window = window
		self.xpos = xpos
		self.ypos = ypos
		self.width = width
		self.height = height
		self.text = text
		self.action = action
		self.image = pg.Surface((width, height))
		self.image.fill((255, 255, 255))
		pg.font.init()
		self.font = pg.font.SysFont('Courier', 36)
		self.text_surface = self.font.render(text, True, (0, 0, 0))
		self.rect = self.image.get_rect(center=(xpos + width / 2, ypos + height / 2))

	def handle_events(self, event):
		if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
			self.action()

	def handle_updates(self):
		pass

	def handle_draws(self):
		self.image.blit(self.text_surface, (
			self.width / 2 - self.text_surface.get_width() / 2, self.height / 2 - self.text_surface.get_height() / 2)
						)
		self.window.screen.blit(self.image, self.rect)


def launch_test_window():
	testWindow = Window((800, 600), 'Test Window')
	testButton1 = Button(testWindow, 100, 100, 250, 50, 'Click me you bum', lambda: print('deez nuts'))
	testButton2 = Button(testWindow, 500, 500, 200, 50, 'Close Window', testWindow.kill)
	testWindow.add_component(testButton1)
	testWindow.add_component(testButton2)
	testWindow.launch_window()

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				testWindow.kill()
				break

		testWindow.wipe()
		for component in testWindow.components:
			component.handle_updates()
			component.handle_draws()

		testWindow.wipe()
		for component in testWindow.components:
			component.handle_updates()
			component.handle_draws()
		testWindow.update_display()
	pg.quit()


launch_test_window()
