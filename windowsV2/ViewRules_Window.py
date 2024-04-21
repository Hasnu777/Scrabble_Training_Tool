import customtkinter as ctk
import os
import webbrowser
from CTkMessagebox import CTkMessagebox

'''Important Variables'''
Exists = False
RulesWindow = None
rules = {
	'NASPA - Site': 'https://scrabbleplayers.org/w/Rules',
	'WESPA - PDF': os.path.join(os.path.dirname(__file__), '../assets\\rules\\wesparulesv4.pdf'),
	'WESPA - Site': 'https://wespa.org/resources#collapse2',
	'FFSc - Site': 'https://www.ffsc.fr/classique.php?page=reglements',
	'FISE - Site': 'https://fisescrabble.org/reglamentos/'
}


# Closes the rules window completely
def destroy():
	RulesWindow.wm_withdraw()
	# window.quit()
	RulesWindow.destroy()
	global Exists
	Exists = False
	Window = None


def focusWindow():
	RulesWindow.focus()


# Takes the rules selected and opens it
def OpenRules(RulesOptions):
	option = RulesOptions.get()
	try:
		webbrowser.open(f'{rules[option]}')  # Opens the rules in the web browser
	except KeyError:
		CTkMessagebox(title='Input Error', message='Invalid Selection', width=160, height=80, sound=True)
	# optionReversed = option[::-1]
	# option = option[:option.index(' ')] + optionReversed[:optionReversed.index(' ')][::-1]  # Removing the ' - ' from the option selected
	# webbrowser.open(f'{rules[option]}')  # Opens the rules in the web browser


# Creates the rules window
def createWindow(master):
	global Exists, RulesWindow
	Exists = True
	RulesWindow = ctk.CTkToplevel(master, width=200, height=40, fg_color='#52342e')  # Creating rules window
	RulesWindow.title('View Rules')
	# Assigns destroy() command to execute when user closes it
	RulesWindow.protocol("WM_DELETE_WINDOW", destroy)
	RulesWindow.resizable(False, False)
	RulesOptions = ctk.CTkComboBox(RulesWindow, values=['NASPA - Site', 'WESPA - PDF', 'WESPA - Site', 'FFSc - Site',
														'FISE - Site'])  # Creates dropbox to select rules
	RulesOptions.place(x=5, y=5)
	OpenRules_Button = ctk.CTkButton(RulesWindow, text='Open', command=lambda: OpenRules(RulesOptions), width=30,
									height=10, fg_color="#8f563b", hover_color="#7b4932")  # Button to open the rules
	OpenRules_Button.place(x=150, y=10)
	RulesWindow.attributes("-topmost", True)
