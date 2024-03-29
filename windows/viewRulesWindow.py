from windows.windowsTemplate import *
from windows import homescreen_window
import os
import webbrowser

rules = {'NASPASite': 'https://scrabbleplayers.org/w/Rules', 'WESPAPDF': os.path.join(os.path.dirname(__file__),
																					  '../assets\\rules\\wesparulesv4.pdf'),
		 'FFScSite': 'https://www.ffsc.fr/classique.php?page=reglements',
		 'FISESite': 'https://fisescrabble.org/reglamentos/'}
rulesOptions = None


def destroyViewRulesWindow(window, master):
	window.destroy()
	homescreen_window.BottomFrame.topLevelWindows['viewRulesWindow'] = None
	unlockFromViewRulesWindow(master)


def unlockFromViewRulesWindow(master):
	for frame in master.frames.values():
		for button in frame.buttons.values():
			button.configure(state='normal')


def lockToViewRulesWindow(master):
	for frame in master.frames.values():
		for button in frame.buttons.values():
			button.configure(state='disabled')


def openRules():
	option = rulesOptions.get()
	optionReversed = option[::-1]
	option = option[:option.index(' ')] + optionReversed[:optionReversed.index(' ')][::-1]
	webbrowser.open(f'{rules[option]}')


def createViewRulesWindow(master):
	viewRulesWindow = ctk.CTkToplevel(master=master, width=200, height=40)
	viewRulesWindow.title('View Rules')
	viewRulesWindow.protocol("WM_DELETE_WINDOW", lambda: destroyViewRulesWindow(viewRulesWindow, master))
	viewRulesFrame = Frame(master=viewRulesWindow, width=200, height=40, xpos=0, ypos=0, fg_color='blue')
	openRulesButton = Button(master=viewRulesFrame, button_text='Open', command=openRules, xpos=150, ypos=10, width=30,
							 height=10)
	global rulesOptions
	rulesOptions = ctk.CTkComboBox(viewRulesFrame, values=['NASPA - Site', 'WESPA - PDF', 'FFSc - Site', 'FISE - Site'])
	rulesOptions.place(x=5, y=5)
	viewRulesWindow.attributes("-topmost", True)
	lockToViewRulesWindow(master=master)
	return viewRulesWindow
