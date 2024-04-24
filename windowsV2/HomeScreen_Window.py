import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os
from windowsV2 import ViewRules_Window
import json


'''Important Variables'''
language = None
Player1 = None
Player2 = None
Filename = None

'''Creating window'''
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


# Closes the home screen window completely
def destroyHomeScreenWindow():
	HomeScreen.wm_withdraw()
	HomeScreen.quit()
	HomeScreen.destroy()


# Creating and calibrating the window
HomeScreen = ctk.CTk(fg_color="#39231f")
HomeScreen.protocol("WM_DELETE_WINDOW", destroyHomeScreenWindow)
HomeScreen.title("Scrabble Tournament Game Hoster v0.1")
HomeScreen.geometry(f"250x210+{HomeScreen.winfo_screenwidth() // 2 - 125}+{HomeScreen.winfo_screenheight() // 2 - 105}")
HomeScreen.resizable(False, False)

# Creates & calibrates a tabview that allows the user to swap between the GUI for a new game, and the GUI to load a game
tabview = ctk.CTkTabview(master=HomeScreen, fg_color="#52342e", segmented_button_unselected_color="#77443b",
						segmented_button_selected_color="#a06144", segmented_button_unselected_hover_color="#522f28",
						segmented_button_selected_hover_color="#7b4932", segmented_button_fg_color="#39231f", width=240,
						height=210)
tabview.place(x=5, y=-5)


# Command to open the rules window
def openRulesWindow():  # Edit viewRulesWindow to get rid of these class templates, IDK how to feel abt them tbh
	if not ViewRules_Window.Exists:  # If the rules window doesn't exist then it will be opened
		ViewRules_Window.createWindow(HomeScreen)  # Opens the rules window
	else:
		ViewRules_Window.focusWindow()  # Makes the rules window the active window


# Button that is used to execute the above command
openRules_Button = ctk.CTkButton(HomeScreen, command=openRulesWindow, text='View Rules', width=40, fg_color="#8f563b",
								hover_color="#7b4932", bg_color='#52342e')
openRules_Button.place(x=85, y=171)

'''New Game Tab'''

newGame = tabview.add("New Game")  # Creates a tabview for the new game GUI to be added to

# Creates entry box to enter Player 1's username
P1Username = ctk.CTkEntry(newGame, placeholder_text="Player 1")
P1Username.place(x=43, y=0)


# Command that retrieves the username from the P1Username entry box
def getP1Username():
	global Player1
	try:
		Player1 = P1Username.get()  # Retrieving username entered in the text box
	except AttributeError:
		pass


# Creates entry box to enter Player 2's username
P2Username = ctk.CTkEntry(newGame, placeholder_text="Player2")
P2Username.place(x=43, y=33)


# Command that retrieves the username from the P2Username entry box
def getP2Username():
	global Player2
	try:
		Player2 = P2Username.get()  # Retrieving password entered in the text box
	except AttributeError:
		pass


# Creates the dropdown box to select the language
chooseLanguage = ctk.CTkComboBox(newGame, values=['English', 'French', 'Spanish'])
chooseLanguage.place(x=43, y=66)


# Command that retrieves the language selected
def getLanguageOption():
	global language
	language = chooseLanguage.get()  # Retrieves language selected from the dropdown box


# Command that retrieves usernames and language selected to start a new game
def startNewGame():
	getP1Username()  # Fetch Player 1 name
	getP2Username()  # Fetch Player 2 name
	getLanguageOption()  # Fetch the language selected
	global language
	# Checking if player names have been entered
	if (Player1 != '' and Player2 != '') and (Player1 is not None and Player2 is not None):
		if Player1 != Player2:  # Checking to make sure the same username hasn't been repeated
			if language is not None:  # Checking if a language has been selected from the dropdown menu
				destroyHomeScreenWindow()
			else:
				# Default value in dropdown menu is English, so this is used if a language isn't selected
				language = 'English'
				destroyHomeScreenWindow()
		else:  # Creates a message box that informs the user of the error
			CTkMessagebox(title='Username Error', message='Error: Username repeated for Player 1 and Player 2',
						width=160, height=80, sound=True)
	else:  # Creates a message box that informs the user of the error
		CTkMessagebox(title='Start Game Error', message='Error: Usernames not entered', width=160, height=80, sound=True)


# Button that executes the above command
newGame_Button = ctk.CTkButton(newGame, width=100, text='Start Game', command=startNewGame, fg_color="#8f563b",
							hover_color="#7b4932")
newGame_Button.place(x=62, y=99)


'''Load Game Tab'''

loadGame = tabview.add("Load Game")  # Creates a tabview for the load game GUI to be added to

# Opens GameData.json to retrieve a list of the game files
with open(os.path.join(os.path.dirname(__file__), '../data/GameData.json')) as f:
	gameData = json.load(f)
	gameFiles = list(gameData.keys())

# Creates a dropdown box to select a game file
selectFileName = ctk.CTkComboBox(loadGame, values=gameFiles)
selectFileName.configure(state='readonly')  # Prevents user from typing inside the dropdown menu
selectFileName.place(x=43, y=10)


# Command that retrieves the selected file name
def getFileName():
	global Filename
	Filename = selectFileName.get()
	destroyHomeScreenWindow()


# Button that executes the above command
loadGame_Button = ctk.CTkButton(loadGame, width=80, text='Load Game', command=getFileName, fg_color="#8f563b",
								hover_color="#7b4932")
loadGame_Button.place(x=72, y=99)


# Command that opens the home screen window
def run():
	HomeScreen.mainloop()
