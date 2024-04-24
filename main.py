import sqlite3
from GameFiles import MainGame
from windowsV2 import HomeScreen_Window
from windowsV2 import LogIn_Window

'''SQL Create Table Statements'''
createAdminTable = '''
	CREATE TABLE IF NOT EXISTS Administrators (
		adminID INTEGER PRIMARY KEY,
		username TEXT NOT NULL UNIQUE,
		password TEXT
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

createAdminGamesTable = '''
	CREATE TABLE IF NOT EXISTS AdminGames (
		gameHostedID INTEGER PRIMARY KEY,
		gameID INTEGER,
		adminID INTEGER,
		FOREIGN KEY (gameID) REFERENCES Games (gameID),
		FOREIGN KEY (adminID) REFERENCES Administrators (adminID)
	)
'''

createPlayerGamesTable = '''
	CREATE TABLE IF NOT EXISTS PlayerGames (
		gamePlayedID INTEGER PRIMARY KEY,
		gameID INTEGER,
		playerID INTEGER,
		FOREIGN KEY (gameID) REFERENCES Games (gameID),
		FOREIGN KEY (playerID) REFERENCES Players (playerID)
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

# Administrators -> AdminGames: One-To-Many
# Players -> PlayerGames: One-To-Many
# AdminGames -> Games: Many-To-One
# PlayerGames -> Games: Many-To-One
# Games -> GameHistory: One-To-Many
# Players -> GameHistory: One-To-Many


def createTable(command):
	conn = sqlite3.connect('ScrabbleTournamentGame.db')  # Connects to database
	cursor = conn.cursor()
	cursor.execute(command)  # runs the command given
	conn.close()


'''Calling createTable() for each of the Create Table statements'''
createTable(createAdminTable)
createTable(createPlayersTable)
createTable(createGamesTable)
createTable(createAdminGamesTable)
createTable(createPlayerGamesTable)
createTable(createGameHistoryTable)

# TODO Create separate sql databases. One to hold above tables, another to hold word lists.

adminID = LogIn_Window.run()  # Retrieving adminID from when the administrator/member of staff logs in
print(adminID, 'adminID fetched from LogIn_Window.py')
language = 'English'  # Default language in case of an unknown error occurring in HomeScreen_Window
# Checking if LogIn_Window has executed with an administrator/member of staff logging in. If not, the program is over.
if adminID is not None:
	HomeScreen_Window.run()
	# Checks if a language has been selected from HomeScreen_Window, as this indicates a new game is starting
	if HomeScreen_Window.language:
		# Starts game instance, passing in the language selected to indicate a new game is being started
		MainGame.CreateGameWindow(adminID, HomeScreen_Window.Player1, HomeScreen_Window.Player2,
									NewGameLang=HomeScreen_Window.language)
	# Checks if a file has been selected from HomeScreen_Window, as this indicates a game is being loaded
	elif HomeScreen_Window.Filename:
		# Starts game instance, passing in the file selected to indicate a game is being loaded
		MainGame.CreateGameWindow(adminID, HomeScreen_Window.Player1, HomeScreen_Window.Player2,
									FileToLoad=HomeScreen_Window.Filename)
# No else statement because it is implied that if neither exist, HomeScreen_Window was closed without doing anything.
# So, the program is over.
