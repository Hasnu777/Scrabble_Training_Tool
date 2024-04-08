import sqlite3

from gameLogic import mainGameV3
from windows import homescreen_window, login_window, createNewGameSettings


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

# createProfilesTable = '''
# 	CREATE TABLE IF NOT EXISTS Users (
# 	userID INTEGER PRIMARY KEY,
# 	username TEXT NOT NULL UNIQUE,
# 	password TEXT
# '''
# #
# createGamesTable = '''
# 	CREATE TABLE IF NOT EXISTS Games (
# 	gameID INTEGER PRIMARY KEY,
# 	userID INTEGER,
# 	language TEXT NOT NULL,
# 	datePlayed DATETIME NOT NULL,
# 	result TEXT NOT NULL,
# 	FOREIGN KEY (userID) REFERENCES Users (userID)
# '''
# #
# createGameParticipantsTable = '''
# 	CREATE TABLE IF NOT EXISTS Game_Participants (
# 	gameID INTEGER,
# 	userID INTEGER,
# 	FOREIGN KEY (gameID) REFERENCES Games (gameID),
# 	FOREIGN KEY (userID) REFERENCES Users (userID),
# 	PRIMARY KEY (gameID, userID)
# '''
#
# def createTable(command):
# 	conn = sqlite3.connect('ScrabbleTournamentGame.db')
# 	cursor = conn.cursor()
# 	cursor.execute(command)
# 	conn.close()
#
#
# createTable(createProfilesTable)
# createTable(createGamesTable)
# createTable(createGameParticipantsTable)


user_id, username = login_window.run()
language = 'English'
if user_id is not None and username is not None:
	homescreen_window.run()
	print('bro.')
	# need to add in case for file name, do this after fixing main window
	if createNewGameSettings.lang:
		mainGameV3.createGameWindow(user_id, createNewGameSettings.lang)
	else:
		mainGameV3.createGameWindow(user_id, language)

# Below are SQL tables to create

# createAdminTable = '''
# 	CREATE TABLE IF NOT EXISTS Administrators (
# 	adminID INTEGER PRIMARY KEY,
# 	username TEXT NOT NULL UNIQUE,
# 	password TEXT
# )
# '''
#
# createGamesTable = '''
# 	CREATE TABLE IF NOT EXISTS Games (
# 	gameID INTEGER PRIMARY KEY,
#   fileName TEXT UNIQUE,
# 	adminID INTEGER,
#   player1_ID INTEGER,
#   player2_ID INTEGER,
# 	language TEXT NOT NULL,
# 	datePlayed DATETIME NOT NULL,
# 	result TEXT NOT NULL,
# 	FOREIGN KEY (adminID) REFERENCES Administrators (adminID),
#     FOREIGN KEY (player1_ID) REFERENCES Players (playerID),
#     FOREIGN KEY (player2_ID) REFERENCES Players (playerID)
# )
# '''
#
# createPlayersTable = '''
# CREATE TABLE IF NOT EXISTS Players (
#     playerID INTEGER PRIMARY KEY,
#     username TEXT NOT NULL,
#     rating INTEGER DEFAULT 1500,
#     gameID INTEGER,
#     FOREIGN KEY (gameID) REFERENCES Games (gameID)
# )
# '''
#
# createGameHistoryTable = '''
# CREATE TABLE IF NOT EXISTS GameHistory (
#     gameID INTEGER,
#     moveNumber INTEGER,
#     playerID INTEGER,
#     words TEXT,
#     score INTEGER,
#     exchanged BOOLEAN NOT NULL,
#     passed BOOLEAN NOT NULL,
#     PRIMARY KEY (gameID, moveNumber),
#     FOREIGN KEY (gameID) REFERENCES Games (gameID),
#     FOREIGN KEY (playerID) REFERENCES Players (playerID)
# )
# '''

# Administrators -> Games: One-To-Many
# Players -> Games: One-To-Many
# Games -> GameHistory/Moves: One-To-Many
# Players -> GameHistory/Moves: One-To-Many