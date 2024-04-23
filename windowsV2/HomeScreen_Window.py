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


# Closes the homescreen window completely
def destroyHomescreenWindow():
	homescreen.wm_withdraw()
	homescreen.quit()
	homescreen.destroy()


# Creating and calibrating the window
homescreen = ctk.CTk(fg_color="#39231f")
homescreen.protocol("WM_DELETE_WINDOW", destroyHomescreenWindow)
homescreen.title("Scrabble Tournament Game Hoster v0.1")
homescreen.geometry(f"250x210+{homescreen.winfo_screenwidth()//2-125}+{homescreen.winfo_screenheight()//2-105}")
homescreen.resizable(False, False)

# Creates & calibrates a tabview that allows the user to swap between the GUI for a new game, and the GUI to load a game
tabview = ctk.CTkTabview(master=homescreen, fg_color="#52342e", segmented_button_unselected_color="#77443b",
						segmented_button_selected_color="#a06144", segmented_button_unselected_hover_color="#522f28",
						segmented_button_selected_hover_color="#7b4932", segmented_button_fg_color="#39231f", width=240,
						height=210)
tabview.place(x=5, y=-5)


# Command to open the rules window
def openRulesWindow():  # Edit viewRulesWindow to get rid of these class templates, IDK how to feel abt them tbh
	if not ViewRules_Window.Exists:  # If the rules window doesn't exist then it will be opened
		ViewRules_Window.createWindow(homescreen)  # Opens the rules window
	else:
		ViewRules_Window.focusWindow()


# Button that is used to execute the above command
openRules_Button = ctk.CTkButton(homescreen, command=openRulesWindow, text='View Rules', width=40, fg_color="#8f563b",
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


# Button that executes the above command
# P1Username_Button = ctk.CTkButton(newGame, text='Enter', width=70, command=getP1Username, fg_color="#8f563b", hover_color="#7b4932")
# P1Username_Button.place(x=180, y=10)

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


# Button that executes the above command
# P2Username_Button = ctk.CTkButton(newGame, text='Enter', width=70, command=getP2Username, fg_color="#8f563b", hover_color="#7b4932")
# P2Username_Button.place(x=180, y=50)


# Creates the dropdown box to select the language
chooseLanguage = ctk.CTkComboBox(newGame, values=['English', 'French', 'Spanish'])
chooseLanguage.place(x=43, y=66)


# Command that retrieves the language selected
def getLanguageOption():
	global language
	language = chooseLanguage.get()  # Retrieves language selected from the dropdown box


# Button that executes the above command
# chooseLanguage_Button = ctk.CTkButton(newGame, text='Select', width=70, command=getLanguageOption, fg_color="#8f563b", hover_color="#7b4932")
# chooseLanguage_Button.place(x=180, y=90)


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
				destroyHomescreenWindow()
			else:
				# Default value in dropdown menu is English, so this is used if a language isn't selected
				language = 'English'
				destroyHomescreenWindow()
		else:  # Creates a message box that informs the user of the error
			CTkMessagebox(title='Username Error', message='Error: Username repeated for Player 1 and Player 2', width=160, height=80, sound=True)
	else:  # Creates a message box that informs the user of the error
		CTkMessagebox(title='Start Game Error', message='Error: Usernames not entered', width=160, height=80, sound=True)
	# Checks if a language is selected and usernames are entered
	# if (Player1 != '') and (Player2 != '') and (language != ''):
	# 	# Checks that the same username isn't entered twice. If not, the game starts and the homescreen window is closed
	# 	if Player1 != Player2:
	# 		homescreen.withdraw()
	# 		homescreen.quit()
	# 		print('kill')
	# 	else:  # Creates a message box that informs the user of the error
	# 		CTkMessagebox(message='Error: Username repeated for Player 1 and Player 2', title='Username Error')
	# else:  # Creates a message box that informs the user of the error
	# 	CTkMessagebox(message='Error: Username not entered or language not chosen', title='Start Game Error')

# completed TO DO: remove enter and select buttons for new game tab view, get startNewGame() to call those functions instead
# this way this prevents username/password/language being entered before swapping to loadgame tabview and then loading a game
# The vice versa is already handled since loadgame fetches the selection from the dropdown menu
# completed TO DO: verify comment just above and ensure that a selection is retrieved each time from dropdown menu upon click of load game button


# Button that executes the above command
newGame_Button = ctk.CTkButton(newGame, width=100, text='Start Game', command=startNewGame, fg_color="#8f563b", hover_color="#7b4932")
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
	destroyHomescreenWindow()


# Button that executes the above command
loadGame_Button = ctk.CTkButton(loadGame, width=80, text='Load Game', command=getFileName, fg_color="#8f563b", hover_color="#7b4932")
loadGame_Button.place(x=72, y=99)


# Command that opens the homescreen window
def run():
	homescreen.mainloop()
