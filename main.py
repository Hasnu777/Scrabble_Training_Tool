import sqlite3

from gameLogic import mainGameV3
from windows import homescreen_window, login_window, createNewGameSettings
from windowsV2 import homescreen_window as hsw


def create_profiles_table():
	conn = sqlite3.connect('scrabbleTrainingTool.db')
	cursor = conn.cursor()

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT NOT NULL UNIQUE,
			password TEXT
	)
	''')

	conn.commit()
	conn.close()


create_profiles_table()

createAdminTable = '''
	CREATE TABLE IF NOT EXISTS Administrators (
	adminID INTEGER PRIMARY KEY,
	username TEXT NOT NULL UNIQUE,
	password TEXT
)
'''

createGamesTable = '''
	CREATE TABLE IF NOT EXISTS Games (
	gameID INTEGER PRIMARY KEY,
	fileName TEXT UNIQUE,
	adminID INTEGER,
	player1_ID INTEGER,
	player2_ID INTEGER,
	language TEXT NOT NULL,
	datePlayed DATETIME NOT NULL,
	result TEXT NOT NULL,
	FOREIGN KEY (adminID) REFERENCES Administrators (adminID),
	FOREIGN KEY (player1_ID) REFERENCES Players (playerID),
	FOREIGN KEY (player2_ID) REFERENCES Players (playerID)
)
'''

createPlayersTable = '''
	CREATE TABLE IF NOT EXISTS Players (
	playerID INTEGER PRIMARY KEY,
	username TEXT NOT NULL,
	gameID INTEGER,
	FOREIGN KEY (gameID) REFERENCES Games (gameID)
)
'''

createGameHistoryTable = '''
	CREATE TABLE IF NOT EXISTS GameHistory (
	gameID INTEGER,
	moveNumber INTEGER,
	playerID INTEGER,
	words TEXT,
	score INTEGER,
	exchanged BOOLEAN NOT NULL,
	passed BOOLEAN NOT NULL,
	PRIMARY KEY (gameID, moveNumber),
	FOREIGN KEY (gameID) REFERENCES Games (gameID),
	FOREIGN KEY (playerID) REFERENCES Players (playerID)
)
'''

# Administrators -> Games: One-To-Many
# Players -> Games: One-To-Many
# Games -> GameHistory/Moves: One-To-Many
# Players -> GameHistory/Moves: One-To-Many


def createTable(command):
	conn = sqlite3.connect('ScrabbleTournamentGame.db')
	cursor = conn.cursor()
	cursor.execute(command)
	conn.close()


createTable(createAdminTable)
createTable(createPlayersTable)
createTable(createGamesTable)
createTable(createGameHistoryTable)


user_id, username = login_window.run()
print(user_id, 'adminID')
print(username, 'admin username')
language = 'English'
if user_id is not None and username is not None:
	# homescreen_window.run()
	hsw.run()
	print('bro.')
	# need to add in case for file name, do this after fixing main window
	if hsw.language:
		mainGameV3.createGameWindow(user_id, hsw.Player1, hsw.Player2, newGameLang=hsw.language)
	elif hsw.Filename:
		mainGameV3.createGameWindow(user_id, hsw.Player1, hsw.Player2, gameFile=hsw.Filename)
