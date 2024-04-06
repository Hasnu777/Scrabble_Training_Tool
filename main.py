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
#
# createGamesTable = '''
# 	CREATE TABLE IF NOT EXISTS Games (
# 	gameID INTEGER PRIMARY KEY,
# 	language TEXT NOT NULL,
# 	datePlayed DATETIME NOT NULL,
# 	result TEXT NOT NULL,
# '''
#
# createGameParticipantsTable = '''
# 	CREATE TABLE IF NOT EXISTS Game_Participants (
# 	gameID INTEGER,
# 	userID INTEGER,
# 	FOREIGN KEY (gameID) REFERENCES Games (gameID),
# 	FOREIGN KEY (userID) REFERENCES Users (userID),
# 	PRIMARY KEY (gameID, userID)
# '''
#
#
# createMovesTable = '''
# 	CREATE TABLE Moves (
# 	moveNumber INTEGER,
# 	gameID INTEGER,
# 	userID INTEGER,
# 	moveMade BLOB,
# 	scoreAwarded INTEGER,
# 	FOREIGN KEY (gameID) REFERENCES Games (gameID),
# 	FOREIGN KEY (userID) REFERENCES Users (userID),
# 	PRIMARY KEY (moveNumber, gameID, userID)
# '''
#
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
	if createNewGameSettings.lang is not None:
		mainGameV3.createGameWindow(createNewGameSettings.lang, user_id)
