# from tkinter import *
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os
import sqlite3 as sql
from windows import viewRulesWindow, viewDictionaryWindow
import json

'''Important Variables'''
language = None
Player1 = None
Player2 = None
Filename = None

'''Creating window'''
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def destroyHomescreenWindow():
	homescreen.wm_withdraw()
	homescreen.quit()


homescreen = ctk.CTk(fg_color="#39231f")
homescreen.protocol("WM_DELETE_WINDOW", destroyHomescreenWindow)
homescreen.title("Scrabble Tournament Game Hoster v0.1")
homescreen.geometry(f"310x256+{homescreen.winfo_screenwidth()//2-155}+{homescreen.winfo_screenheight()//2-128}")
homescreen.resizable(False, False)

tabview = ctk.CTkTabview(
	master=homescreen,
	fg_color="#52342e",
	segmented_button_unselected_color="#77443b",
	segmented_button_selected_color="#a06144",
	segmented_button_unselected_hover_color="#522f28",
	segmented_button_selected_hover_color="#7b4932",
	segmented_button_fg_color="#39231f")
tabview.place(x=5, y=0)


def openRulesWindow():  # Edit viewRulesWindow to get rid of these class templates, IDK how to feel abt them tbh
	if not viewRulesWindow.Exists:
		viewRulesWindow.createViewRulesWindow(homescreen)


openRules_Button = ctk.CTkButton(homescreen, command=openRulesWindow, text='View Rules', width=40, fg_color="#8f563b", hover_color="#7b4932", bg_color='#52342e')
openRules_Button.place(x=10, y=216)


def openDictionaryWindow():
	if not viewDictionaryWindow.Exists:
		viewDictionaryWindow.createViewDictionaryWindow(homescreen)


openDictionary_Button = ctk.CTkButton(homescreen, command=openDictionaryWindow, text='View Dictionary', width=60, fg_color="#8f563b", hover_color="#7b4932", bg_color='#52342e')
openDictionary_Button.place(x=197, y=216)


'''New Game Tab'''

newGame = tabview.add("New Game")


def getP1Username():
	global Player1
	try:
		Player1 = P1Username.get()
	except AttributeError:
		pass


P1Username = ctk.CTkEntry(newGame, placeholder_text="Player 1")
P1Username.place(x=35, y=10)
P1Username_Button = ctk.CTkButton(newGame, text='Enter', width=70, command=getP1Username, fg_color="#8f563b", hover_color="#7b4932")
P1Username_Button.place(x=180, y=10)


def getP2Username():
	global Player2, P2Username
	try:
		Player2 = P2Username.get()
	except AttributeError:
		pass


P2Username = ctk.CTkEntry(newGame, placeholder_text="Player2")
P2Username.place(x=35, y=50)
P2Username_Button = ctk.CTkButton(newGame, text='Enter', width=70, command=getP2Username, fg_color="#8f563b", hover_color="#7b4932")
P2Username_Button.place(x=180, y=50)


def getLanguageOption():
	global language
	language = chooseLanguage.get()


# chooseLanguage_var = ctk.StringVar(value='Choose Language')
chooseLanguage = ctk.CTkComboBox(newGame, values=['English', 'French', 'Spanish'])
chooseLanguage.place(x=35, y=90)
# chooseLanguage_var.set('Choose Language')

chooseLanguage_Button = ctk.CTkButton(newGame, text='Select', width=70, command=getLanguageOption, fg_color="#8f563b", hover_color="#7b4932")
chooseLanguage_Button.place(x=180, y=90)


def startNewGame():
	if (Player1 != '') and (Player2 != '') and (language != ''):
		if Player1 != Player2:
			homescreen.withdraw()
			homescreen.quit()
			print('kill')
		else:
			CTkMessagebox(message='Error: Username repeated for Player 1 and Player 2', title='Username Error')
	else:
		CTkMessagebox(message='Error: Username not entered or language not chosen', title='Start Game Error')
		# alter design of window maybe IDK


newGame_Button = ctk.CTkButton(newGame, width=100, text='Start Game', command=startNewGame, fg_color="#8f563b", hover_color="#7b4932")
newGame_Button.place(x=80, y=174)


'''Load Game Tab'''

loadGame = tabview.add("Load Game")

gameFiles = []

with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
	cursor = conn.cursor()
	cursor.execute('SELECT fileName FROM Games')
	files = cursor.fetchall()
	for file in files:
		if file[0] is not None and file[0] != '':
			gameFiles.append(file[0])

# with open(os.path.join(os.path.dirname(__file__), '../data/GameData.json')) as f:
# 	gameData = json.load(f)
# 	gameFiles = list(gameData.keys())

selectFileName = ctk.CTkComboBox(loadGame, values=gameFiles)
selectFileName.place(x=75, y=20)


def getFileName():
	global Filename
	Filename = selectFileName.get()
	destroyHomescreenWindow()
#
#
# enterFileName = ctk.CTkEntry(loadGame, placeholder_text='Enter file name...')
# enterFileName.place(x=75, y=20)


# Providing list shouldn't be too hard: get all file names via SQL connection, create list out of cursor.fetchall() and shove into CTkComboBox() then alter getFile() to handle that appropriately
# def getFile():  # can't test this since I haven't made the SQL table, but I don't see why it wouldn't work
# 	global Filename
# 	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
# 		cursor = conn.cursor()
# 		cursor.execute('SELECT fileName FROM Games where fileName=?', (enterFileName.get(),))
# 		nameFetched = cursor.fetchone()[0]
# 		if nameFetched != '':
# 			Filename = nameFetched
# 			# homescreen.destroy()
# 		else:
# 			CTkMessagebox(message='Error: Invalid file name', title='File Name Error')


loadGame_Button = ctk.CTkButton(loadGame, width=80, text='Load Game', command=getFileName, fg_color="#8f563b", hover_color="#7b4932")
loadGame_Button.place(x=105, y=70)

# '''View Info Tab'''

# viewInfo = tabview.add("View Info")
#
# viewInfo_Button = ctk.CTkButton(viewInfo).place(x=30, y=20)


def run():
	homescreen.mainloop()
	homescreen.destroy()

# TODO: go through loadgame and fix errors e.g. game not starting until you click fill rack and pause button to
#  pause/resume, player timer not loading until its their turn, i think there's some score allocation issue as well? Look into this56

