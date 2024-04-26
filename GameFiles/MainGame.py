import pygame as pg
import pygame_gui as pg_gui
import sqlite3 as sql
import random
import os
import json
from GameFiles import ScrabbleItemTemplates
from datetime import datetime


# Creating the game board, player objects, and tile bag
def StartNewGame(language, P1Name, P2Name):

	# Creating Board
	GameBoard = ScrabbleItemTemplates.Board((400, 10))

	# Adding text for premium squares to the board
	GameBoard = AddSpecialLocations(GameBoard, language)
	# Creating Tile Bag
	TileBag = ScrabbleItemTemplates.TileBag((50, 250), language)

	# Creating Player 1
	Player1 = ScrabbleItemTemplates.Player(P1Name, (550, 775), (1180, 750), (1180, 720))

	# Creating Player 2
	Player2 = ScrabbleItemTemplates.Player(P2Name, (550, 775), (1180, 75), (1180, 45))

	return GameBoard, Player1, Player2, TileBag


# Creating new Square objects for premium squares, that contain the premium square type
def AddSpecialLocations(board, language):
	for bonusType in ScrabbleItemTemplates.SpecialLocations.keys():  # Goes through each type of premium square
		for position in ScrabbleItemTemplates.SpecialLocations[bonusType]:  # Goes through each coordinate pair
			# Checks the game language to give the appropriate abbreviation to denote the premium square type.
			match language:
				case 'French':
					if bonusType == 'DL':
						bonusType = 'LD'
					if bonusType == 'DW':
						bonusType = 'MD'
					if bonusType == 'TL':
						bonusType = 'LT'
					if bonusType == 'TW':
						bonusType = 'MT'
				case 'Spanish':
					if bonusType == 'DW':
						bonusType = 'DP'
					if bonusType == 'TW':
						bonusType = 'TP'
				case _:  # the keys for ScrabbleItemTemplates.SpecialLocations is the English version, hence pass
					pass
			board.addToBoard(position[0], position[1], bonusType)  # Adds the premium square type to the board
			# Creates a Square object and adds it to the board
			board.squares[position[0]][position[1]] = ScrabbleItemTemplates.Square(
				((448 + position[1] * 48), (58 + position[0] * 48)), text=bonusType)
	return board


# Loading a game from a JSON file
def LoadGame(file):
	# Loading game information from the file
	with open(os.path.join(os.path.dirname(__file__), f'../data\\{file}.json')) as f:
		gameData = json.load(f)

	# Retrieving the game's language
	language = gameData['Tile Bag']['Language']

	board = list(gameData['Board'].values())  # Retrieving the board
	GameBoard = ScrabbleItemTemplates.Board((400, 10))  # Loading the Board object
	GameBoard = AddSpecialLocations(GameBoard, language)  # Getting the Square objects for premium squares
	GameBoard.replaceBoard(board)  # Updating the board

	bag = gameData['Tile Bag']['Bag']  # Retrieving tile bag contents
	isEmptyFlag = bag.pop()
	random.shuffle(bag)  # It's not realistic to assume the tile bag has been untouched if an actual game were to be
	# paused, so it should be shuffled.
	bag.append(isEmptyFlag)
	TileBag = ScrabbleItemTemplates.TileBag((50, 250), language)  # Loading TileBag object
	TileBag.replaceBag(bag)  # Updating tile bag
	TileBag.shuffleCount = 2

	# Iterating through the board to update the board's sprites, so that Tile objects are shown on the board
	for row in range(15):
		for column in range(15):
			# Checking if the board position has a tile
			if GameBoard.getBoard()[row][column] in TileBag.alphabet:
				# Creating the Tile object
				tile = ScrabbleItemTemplates.Tile(f'{language}Letters\\TILE_{GameBoard.getBoard()[row][column]}.png',
													(448+column*48, 58+row*48), GameBoard.getBoard()[row][column],
													TileBag.lexicon[GameBoard.getBoard()[row][column]])
				tile.transformImage((32, 32))  # Shrinking the tile so it fits in the board
				tile.canBeClicked = False  # Ensuring the tile cannot be interacted with
				GameBoard.squares[row][column] = tile  # Putting the Tile object in the board's sprites/text array
				GameBoard.addToGroup(tile)  # Putting the Tile object in the board's group

	# Retrieving Player 1 information
	P1Name = gameData['Player 1']['Name']
	P1Rack = gameData['Player 1']['Rack']
	P1Score = gameData['Player 1']['Score']
	P1TimeLeft = gameData['Player 1']['Timer']['Time Left']
	P1Overtime = gameData['Player 1']['Timer']['Overtime']

	Player1 = ScrabbleItemTemplates.Player(P1Name, (550, 775), (1180, 750),
											(1180, 720))
	Player1.rack.replaceContents(P1Rack)
	Player1.rack.fillRackGroup(language, TileBag.lexicon)
	Player1.score.updateScore(P1Score)
	Player1.timer.currentSeconds = P1TimeLeft
	Player1.timer.isOvertime = P1Overtime

	# Updating the timer to show the correct time
	if P1Overtime:
		Player1.timer.updateOvertimeTimer()
	else:
		Player1.timer.updateTimer()

	# Retrieving Player 2 information
	P2Name = gameData['Player 2']['Name']
	P2Rack = gameData['Player 2']['Rack']
	P2Score = gameData['Player 2']['Score']
	P2TimeLeft = gameData['Player 2']['Timer']['Time Left']
	P2Overtime = gameData['Player 2']['Timer']['Overtime']

	Player2 = ScrabbleItemTemplates.Player(P2Name, (550, 775), (1180, 75),
											(1180, 45))
	Player2.rack.replaceContents(P2Rack)
	Player2.rack.fillRackGroup(language, TileBag.lexicon)
	Player2.score.updateScore(P2Score)
	Player2.timer.currentSeconds = P2TimeLeft
	Player2.timer.isOvertime = P2Overtime

	# Update the timer to show the correct time
	if P2Overtime:
		Player2.timer.updateOvertimeTimer()
	else:
		Player2.timer.updateTimer()

	Flags = list(gameData['Flags'].values())

	return GameBoard, TileBag, Player1, Player2, Flags, P1Name, P2Name


# Retrieve playerID for a player
def GetPlayerID(username):
	# Open a connection to the SQL database
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT playerID FROM Players WHERE username=?', (username,))
		userID = cursor.fetchone()  # Getting the first record retrieved by the SQL query
		if userID:  # Triggers if a userID shows up
			return userID[0]  # userID would look like ('<userID>',), so [0] gets '<userID>'
		else:
			# Creating a record of the player and then fetching the userID
			cursor.execute('''INSERT INTO Players ('username') VALUES (?)''', (username,))
			cursor.execute('''SELECT playerID FROM Players WHERE username=?''', (username,))
			# Returning the playerID. Guaranteed to select the playerID after creating a record with that username
			return cursor.fetchone()[0]


# Retrieve gameID of the game
def GetGameID(file):
	# Opening connection to SQL database
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		# Fetching gameID
		cursor.execute('SELECT gameID FROM Games WHERE fileName=?', (file,))
		# gameID is guaranteed to be fetched, since file selection dropdown menu is read-only, so you must select an
		# option from the dropdown menu. Those options exist because they've been saved, so they all have a gameID.
		return cursor.fetchone()[0]


# Retrieve a single tile per player, to determine the player order
def DetermineOrder(TileBag):
	item = random.choice(TileBag.bag[:-1])  # Retrieving information of a random tile
	return item[0]  # Returning the letter of that tile


# Swapping Players around (TEST IF REQUIRED, GO WITHOUT AND PRINT OUT INFO BEFORE N AFTER SWAP)
def SwapPlayers(Player1, Player2, P1Name, P2Name, P1_ID, P2_ID):
	return Player2, Player1, P2Name, P1Name, P2_ID, P1_ID


# Filling each player's rack at the beginning of a game
def FillRacks(P1Rack, P2Rack, TileBag):
	P1Rack.fillRack(TileBag)  # Filling Player 1 Rack
	P1Rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)  # Filling sprites array for Player 1's rack

	P2Rack.fillRack(TileBag)  # Filling Player 2's rack
	P2Rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)  # Filling sprites array for Player 2's rack


# Adding a game to the Games table
def CreateGameRecord(adminID, P1_ID, P2_ID):
	# Opening a connection to the SQL database
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		current_time = datetime.now()  # Getting the current date and time
		cursor.execute('''INSERT INTO Games ('datePlayed') VALUES (?)''', (current_time,))
		cursor.execute('''SELECT gameID FROM Games WHERE datePlayed=?''', (current_time,))
		gameID = cursor.fetchone()[0]  # Retrieving gameID from cursor
		# Recording the game for the administrator
		cursor.execute('''INSERT INTO AdminGames ('gameID', 'adminID') VALUES (?, ?)''',
						(gameID, adminID,))
		# Recording the game for the first player name entered from the main menu
		cursor.execute('''INSERT INTO PlayerGames ('gameID', 'playerID') VALUES (?, ?)''',
						(gameID, P1_ID,))
		# Recording the game for the second player name entered from the main menu
		cursor.execute('''INSERT INTO PlayerGames ('gameID', 'playerID') VALUES (?, ?)''',
						(gameID, P2_ID,))
		return gameID


# Selecting a Tile from the player's rack
def SelectTile(Player, mouse_pos):
	# Going through the sprites array of the player's rack, to get the sprite, and it's position in the rack
	for i, tile in enumerate(Player.rack.getSprites().values()):
		# Checking if a sprite was retrieved
		if tile:
			# Checking if the mouse's click position was within a Tile's effective area
			if tile.getRect().collidepoint(mouse_pos) and tile.canBeClicked:
				tile.isClicked = True  # Showing that the tile was successfully selected
				if tile.getLetter() == '!':  # Checking if the tile selected is a blank tile
					return True, True  # True for a tile being selected, and True for a blank tile being selected
				else:
					return True, False  # True for a tile being selected, and False for a blank tile being selected
			else:
				continue  # A tile hasn't been selected, so a blank tile also hasn't been selected
	return False, False  # In the event there are no Tile objects in the rack's sprites array, no tile can be selected


# Selecting a board position to place a tile
def SelectSquare(board, mouse_pos):
	for i in range(225):
		try:
			# Type declaration to force an exception in the event the player clicks on a tile on the board
			square: ScrabbleItemTemplates.Square = board.squares[i // 15][i % 15]
			# Checking if the mouse's click position was within a Square's effective area
			if square.getSquareRect().collidepoint(mouse_pos):
				return i // 15, i % 15
		except AttributeError:  # The item loaded from board.squares was not a Square object
			continue
	return -1, -1  # Shows that the player clicked on the board, but not on a square of the board


# Retrieving the tile that needs to be moved
def GetSelectedTile(Player, tilesPlaced):
	# Iterating through the sprites in the sprites array of the player's rack, and their positions in the rack
	for i, tile in enumerate(Player.rack.getSprites().values()):
		if tile:  # Checks if this actually holds a Tile object, or is None.
			if tile.isClicked:  # If the tile's been selected
				tile.isClicked = False  # De-selects the tile
				Player.rack.removeFromRack(i, tile)  # Takes the tile out of the rack
				tilesPlaced.append((i, tile))  # Holds the tile in the move stack
				return False, tilesPlaced


# Moving the selected tile from the rack to the board
def PlaceTile(GameBoard, row, column, tilesPlaced):
	tile = tilesPlaced[-1][1]
	squareType = GameBoard.GetSquare(row, column)  # Retrieving the square type
	GameBoard.addToBoard(row, column, tile.getLetter())  # Putting the tile in the board array
	square = GameBoard.squares[row][column]  # Putting the tile's sprite in the board's sprites/text array
	tile.updateRect(square.getRectCoordinates())  # Moving the tile sprite to the selected square
	tile.transformImage((32, 32))  # Shrinking the tile sprite's image and effective area to fit within the square
	tile.isClicked = False  # De-selecting the tile
	tile.canBeClicked = False  # Preventing the tile from being interacted with
	GameBoard.squares[row][column] = tile  # Adding the tile sprite to the board's sprites/text array
	GameBoard.addToGroup(tile)  # Adding the tile sprite to the board's group
	# Filling the stack entry for tilesPlaced
	tilesPlaced[-1] = (tilesPlaced[-1][0], tile, squareType, square, row, column)
	return GameBoard, tilesPlaced


# Exchanging the selected tile
def ExchangeTile(Player, TileBag):

	tileToExchange = None
	tileToExchangePosition = None
	# Iterates through the rack positions and values in the sprites array
	for i, tile in enumerate(Player.rack.getSprites().values()):
		if tile is not None:  # Checks if a Tile object has been revealed
			if tile.isClicked:  # Checks if the tile has been clicked
				tileToExchange = tile
				tileToExchangePosition = i
				break

	if tileToExchange:
		Player.rack.removeFromRack(tileToExchangePosition, tileToExchange)  # Removing the tile from the rack
		Player.rack.fillRack(TileBag)  # Getting a new tile for the rack
		Player.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)  # Getting a new tile
		sprites = Player.rack.getSprites()  # Getting the sprites array
		newTile = sprites[f'TILE{tileToExchangePosition+1}']  # Getting the new Tile sprite out of the sprites array
		newTile.updateImage('TILE_UNKNOWN.png')  # Hiding the tile information from the player
		newTile.canBeClicked = False
		sprites[f'TILE{tileToExchangePosition+1}'] = newTile  # Updating the sprites array with the modified Tile sprite
		Player.rack.updateSprites(sprites)  # Updating the sprites array
		Player.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)
	return Player, TileBag, False  # Returning False for a tile being selected


# Assign a letter to the blank tile placed on the board
def DesignateBlank(GameBoard, tilesPlaced, language, letter):
	lastMove = tilesPlaced[-1]
	tile = lastMove[1]  # Getting the blank tile that was placed
	GameBoard.removeFromGroup(tile)  # Removing the Tile sprite from the game board's group
	tile.updateLetter(letter)  # Designating the letter
	tile.updateImage(f'{language}Letters\\TILE_{letter}_BLANK.png')  # Updating the image to reflect the designation.
	tile.transformImage((32, 32))  # Shrinking the image and the Tile sprite's effective area, so it fits in the board
	GameBoard.getBoard()[lastMove[-2]][lastMove[-1]] = letter  # Updating the designation for the board
	GameBoard.addToGroup(tile)  # Adding the modified Tile sprite back to the board group
	# Updating the move stack with the modified Tile
	lastMove = (lastMove[0], tile, lastMove[2], lastMove[3], lastMove[4], lastMove[5])
	tilesPlaced[-1] = lastMove  # Over-writing the last stack entry with it's updated version
	return GameBoard, tilesPlaced, False  # Returning False to deactivate the flag for a blank tile being clicked


# Undoes the player's play, by recalling tiles back to the rack and putting Square objects back on the board
def UndoPlay(GameBoard, Player, language, tilesPlaced, i=0):
	i += 1
	if not tilesPlaced:  # Checking if the stack is empty:
		return GameBoard, tilesPlaced, Player  # Stopping condition has been met, so the subroutine unravels itself
	rackPosition, tile, squareType, square, row, column = tilesPlaced.pop()  # Removes the stack entry information
	GameBoard.removeFromGroup(tile)  # Removing the tile from the board
	GameBoard.squares[row][column] = square  # Putting the Square object back in board's sprites/text array
	if tile.getScore() == 0:  # Checking if the tile is a blank, since it's score is always 0
		# Updating the tile to look like a blank tile. Also updates the rect/effective area to fit within the rack.
		tile.updateLetter('!')
		tile.updateImage(f'{language}Letters\\TILE_!.png')
	else:
		# Putting the image back to its original size, and updating the rect/effective area to fit within the rack
		tile.updateImage(f'{language}Letters\\TILE_{tile.getLetter()}.png')
	tile.updateRect((584+rackPosition*64, 798))  # Moving the Tile sprite back to it's position in the rack
	tile.canBeClicked = True
	GameBoard.getBoard()[row][column] = squareType  # Putting the square type back in the actual board
	Player.rack.addToRack(rackPosition, tile)  # Adds the tile to the player's rack at the selected rack position
	# Subroutine calls itself so that all moves in the play are undone
	return UndoPlay(GameBoard, Player, language, tilesPlaced, i)


# Mergesort algorithm main section
def MergeSort(listToSort):
	if len(listToSort) <= 1:  # List will not require sorting
		return listToSort

	# Split the provided list into two halves
	midpoint = len(listToSort) // 2
	leftHalf = listToSort[:midpoint]
	rightHalf = listToSort[midpoint:]

	# Apply the merge sort algorithm to each half
	leftHalf = MergeSort(leftHalf)
	rightHalf = MergeSort(rightHalf)

	# Return the full list in its sorted form
	return MergeSortedHalves(leftHalf, rightHalf)


# Merging two sorted lists into one sorted list
def MergeSortedHalves(leftHalf, rightHalf):
	sortedList = []
	i = j = 0

	# Combining the sorted halves into one full list
	while i < len(leftHalf) and j < len(rightHalf):
		if leftHalf[i] < rightHalf[j]:
			sortedList.append(leftHalf[i])
			i += 1
		else:
			sortedList.append(rightHalf[j])
			j += 1

	# Adding the remainders for each half (if present)
	sortedList.extend(leftHalf[i:])
	sortedList.extend(rightHalf[j:])

	return sortedList


# Checks if one list has elements found in another list, in the same oder
def CheckIfSublist(lst1, lst2):
	startingPosition = lst1[0]  # Gets the first number of lst1
	endPosition = lst1[-1]  # Gets the last number of lst 1
	# Checks if lst1 is the same as the spliced lst2, spliced between the first and last number collected (inclusive)
	# Returns that Boolean value
	return lst1 == lst2[startingPosition:endPosition+1]


# Checking if tiles are placed in a: single string of tiles, one tile covers the center square if it's the first play
def CheckValidPlacement(GameBoard, alphabet, tilesPlaced, firstTurn):
	validPlay = False
	RowsIsSublist = False
	ColumnsIsSublist = False

	rowsAndColumns = [(move[4], move[5]) for move in tilesPlaced]  # Takes the row and column of each newly placed tile
	rows = [move[4] for move in tilesPlaced]  # takes the row of each newly placed tile
	columns = [move[5] for move in tilesPlaced]  # Takes the column of each newly placed tile
	correctionRequired = False

	allRowsOrColumns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

	if len(rowsAndColumns) > 0:  # Checks if tiles have been placed, shown by rows and columns being retrieved
		# Checks if all rows are the same, or all columns are the same. Done to see if tiles are placed in one string.
		if not (rows.count(rows[0]) == len(rows) or columns.count(columns[0]) == len(columns)):
			return False, False  # Returns False for validPlay, and False to show that words were formed
		else:
			if rows.count(rows[0]) == len(rows):
				# Checking if all the tiles are placed together without column gaps
				columns = MergeSort(columns)  # Sorted the column values to put them in ascending order
				# If there are gaps in columns, check if there are tiles present for the missing columns. If there are,
				# those tiles were there before the current play, meaning a single string of tiles has been made.
				missingColumns = [number for number in allRowsOrColumns[columns[0]:(columns[-1]+1)]
								if number not in columns]
				for number in missingColumns:
					correctionRequired = GameBoard.getBoard()[rows[0]][number] in alphabet
				if correctionRequired:
					for number in missingColumns:
						columns.append(number)
						columns = MergeSort(columns)
				ColumnsIsSublist = CheckIfSublist(columns, allRowsOrColumns)
			elif columns.count(columns[0]) == len(columns):
				# Checking if all the tiles are placed together without row gaps
				rows = MergeSort(rows)
				missingRows = [number for number in allRowsOrColumns[rows[0]:(rows[-1]+1)]
								if number not in rows]
				for number in missingRows:
					correctionRequired = GameBoard.getBoard()[number][columns[0]] in alphabet
				if correctionRequired:
					for number in missingRows:
						rows.append(number)
						rows = MergeSort(rows)
				RowsIsSublist = CheckIfSublist(rows, allRowsOrColumns)
		if firstTurn and (RowsIsSublist or ColumnsIsSublist):  # Checking if the first turn has been played
			# Checking if there is a tile placed on the center square
			for move in tilesPlaced:
				if move[1].getRectCoordinates() == (784, 394):  # If the Tile sprite is at the center square
					validPlay = True
					break
			return validPlay, True  # True to show that words were formed
		elif not firstTurn and (RowsIsSublist or ColumnsIsSublist):
			for move in tilesPlaced:
				# Goes through information in the move stack for each tile placed If statements below will check the
				# squares on either side & above/below the tile placed, to see if there is a tile that connects to the
				# tile. It then checks if the row and column of that connecting tile isn't in rowsAndColumns, because
				# this means that the connecting tile was not newly placed. Hence, the string of tiles is placed in a
				# valid manner. Has an outer if statement to ensure that the altered index position is within the range
				# of the board's rows/columns
				if move[4] - 1 >= 0:  # Checks if the row to check is within bounds
					squareToCheck = GameBoard.getBoard()[move[4] - 1][move[5]]  # To get the square above
					if squareToCheck in alphabet and (move[4] - 1, move[5]) not in rowsAndColumns:
						validPlay = True
						break
				if move[5] - 1 >= 0:  # Checks if the column to be accessed is within bounds
					squareToCheck = GameBoard.getBoard()[move[4]][move[5] - 1]  # To get the square to the left
					if squareToCheck in alphabet and (move[4], (move[5] - 1)) not in rowsAndColumns:
						validPlay = True
						break
				if move[4] + 1 <= 14:  # Checks if the row to be accessed is within bounds
					squareToCheck = GameBoard.getBoard()[move[4] + 1][move[5]]  # To get the square below
					if squareToCheck in alphabet and (move[4] + 1, move[5]) not in rowsAndColumns:
						validPlay = True
						break
				if move[5] + 1 <= 14:  # Checks if the column to be accessed is within bounds
					squareToCheck = GameBoard.getBoard()[move[4]][move[5] + 1]  # To get the square to the right
					if squareToCheck in alphabet and (move[4], (move[5] + 1)) not in rowsAndColumns:
						validPlay = True
						break
			return validPlay, True  # True to show that words were formed
		else:
			# False to show that tiles were placed incorrectly, False because any words formed are irrelevant
			return False, False
	else:
		return True, False  # Returns True for validPlay, False for words formed
		# This is because this shows that the user has skipped their turn & not made any moves


# Collecting all new words placed on the board
def CollectWordsPlayed(GameBoard, alphabet, language, WordsPlayed):
	board = GameBoard.getBoard()  # Gets the board

	wordsOnBoard = [[], []]  # 2D array to store words created horizontally, and words created vertically
	wordsInRow = ''
	for row in board:
		for letter in row:  # 2 for loops used to go through each square in the board, left to right, row-wise
			if letter in alphabet:  # Checks if the item stored at that position is a letter of the alphabet
				wordsInRow += letter  # Appends said letter to the wordsInRow string
			else:  # Triggers if the item stored is ' ', or denotes a premium square e.g. TW, DW, LD, etc.
				# Checks language to perform the correct validation checks on the letters collected
				if language == 'English':
					# Checks if the string is 2 characters in length, and not in the below tuple
					if len(wordsInRow) > 1 and wordsInRow not in ('RR', 'LL'):
						# If checks are passed, the letters collected are added to wordsOnBoard
						wordsOnBoard[0].append(wordsInRow)
				else:
					# If language is not English it uses this tuple, which has 'CH' as an extra string.
					# 'CH' wasn't in the above tuple because CH is a valid 2-letter word in English Scrabble
					if len(wordsInRow) > 1 and wordsInRow not in ('CH', 'RR', 'LL'):
						# If checks are passed, the letters collected are added to wordsOnBoard
						wordsOnBoard[0].append(wordsInRow)
				wordsInRow = ''  # Resets, so it doesn't carry the letters from the last scan portion
		# Used to add the very last letters scanned off the board. Has the same validation checks as above.
		if language == 'English':
			if len(wordsInRow) > 1 and wordsInRow not in ('RR', 'LL'):
				wordsOnBoard[0].append(wordsInRow)
		else:
			if len(wordsInRow) > 1 and wordsInRow not in ('CH', 'RR', 'LL'):
				wordsOnBoard[0].append(wordsInRow)

	wordsInColumn = ''
	for column in range(15):
		for row in range(15):  # for loops used to go through the columns of the board.
			if board[row][column] in alphabet:  # Checks if the square at this position has a letter
				wordsInColumn += board[row][column]  # Adds the letter to the string
			else:  # Triggers if the item stored is ' ', or denotes a premium square e.g. TW, DW, LD, etc.
				# Checks language to perform the correct validation checks on the letters collected
				if language == 'English':
					# Checks if the string is 2 characters in length, and not in the below tuple
					if len(wordsInColumn) > 1 and wordsInColumn not in ('RR', 'LL'):
						# If checks are passed, the letters collected are added to wordsOnBoard
						wordsOnBoard[1].append(wordsInColumn)
				else:  # If language is not English it uses this tuple, which has 'CH' as an extra string.
					# 'CH' wasn't in the above tuple because CH is a valid 2-letter word in English Scrabble
					if len(wordsInColumn) > 1 and wordsInColumn not in ('CH', 'RR', 'LL'):
						# If checks are passed, the letters collected are added to wordsOnBoard
						wordsOnBoard[1].append(wordsInColumn)
				wordsInColumn = ''  # Resets, so it doesn't carry letters from the last scan portion
		# Used to add the very last letters scanned off the board. Has the same validation checks as above.
		if language == 'English':
			if len(wordsInColumn) > 1 and wordsInColumn not in ('RR', 'LL'):
				wordsOnBoard[1].append(wordsInColumn)
		else:
			if len(wordsInColumn) > 1 and wordsInColumn not in ('CH', 'RR', 'LL'):
				wordsOnBoard[1].append(wordsInColumn)
		wordsInColumn = ''

	wordsCreated = [[], []]  # Used to store all the newly made words

	# Going through words made horizontally
	for word in wordsOnBoard[0]:
		# If a word in wordsOnBoard[0] exists more times than in wordsPlayed, it's a newly created word.
		if wordsOnBoard[0].count(word) > WordsPlayed[0].count(word):
			# For loop to add that word the amount of times the word has been created
			for i in range(wordsOnBoard[0].count(word) - WordsPlayed[0].count(word)):
				wordsCreated[0].append(word)

	# Going through words made vertically
	for word in wordsOnBoard[1]:
		# If a word in wordsOnBoard[1] exists more times than in wordsPlayed, it's a newly created word.
		if wordsOnBoard[1].count(word) > WordsPlayed[1].count(word):
			# For loop to add that word the amount of times the word has been created
			for i in range(wordsOnBoard[1].count(word) - WordsPlayed[1].count(word)):
				wordsCreated[1].append(word)

	return wordsCreated, wordsOnBoard


# Checking if the words placed are valid
def CheckWords(WordsToCheck, language):
	# Opening a connection to the SQL database, to access the word tables
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		# Used to go through the array of horizontally made words, and the vertically made words
		for row in WordsToCheck:
			for word in row:  # For loop to go through each word
				# Fetches the word from the word table
				cursor.execute(f'SELECT words FROM {language}Words WHERE words=?', (word,))
				wordFetched = cursor.fetchone()
				if wordFetched is None:  # Checks if a word was actually fetched
					return False
		# if word != wordFetched[0]: UNSURE IF THIS IS NEEDED HONESTLY
		# 	return False
	return True


# Calculate the score of all the words formed from a play
def CalculateScore(wordsCreated, tilesPlaced, lexicon):  # (rackPosition, tile, squareType, square, row, column)
	wordsInRow = wordsCreated[0]  # Takes the horizontally formed words
	wordsInColumn = wordsCreated[1]  # Takes the vertically formed words
	wordsInRowAndScores = []  # Should store tuples, of the word and its score
	wordsInColumnAndScores = []  # Should store tuples, of the word and its score
	score = 0

	# Get score of words horizontally formed
	for word in wordsInRow:
		for letter in word:  # 2 for loops to go through each letter and get it's raw score
			score += lexicon[letter][0]
		wordsInRowAndScores.append((word, score))
		score = 0

	# Get scores of words vertically formed
	for word in wordsInColumn:
		for letter in word:
			score += lexicon[letter][0]
		wordsInColumnAndScores.append((word, score))
		score = 0

	'''The 3 for loops below correct the score of horizontally formed words'''
	# Corrects score by removing incorrectly added scores from blank tiles
	for move in tilesPlaced:  # Going through stack entries in the move stack
		# Iterate through the index positions and tuples in wordsInRowAndScores
		for i, wordAndScore in enumerate(wordsInRowAndScores):
			# Checks if the letter of the tile placed is in the word AND if the score of the tile placed is 0
			# This is done because score isn't altered, to show that the tile was originally a blank tile
			if move[1].getLetter() in wordAndScore[0] and move[1].getScore() == 0:
				# Updates the wordAndScore by removing the value of the letter being represented by the blank tile
				wordsInRowAndScores[i] = (wordAndScore[0], (wordAndScore[1]-lexicon[move[1].getLetter()][0]))

	# Corrects score by activating letter multipliers
	for move in tilesPlaced:  # Going through stack entries in the move stack
		# Iterate through the index position and tuples in wordsInRowAndScores
		for i, wordAndScore in enumerate(wordsInRowAndScores):
			# Checking if the letter of the tile placed is in the word
			if move[1].getLetter() in wordAndScore[0]:
				# Checking if the square in which the tile was placed is a premium square that boosts letter score
				if move[2] in ('DL', 'LD'):
					# Increases the score of that word by adding the letter's value again (added twice in total)
					wordsInRowAndScores[i] = (wordAndScore[0], (wordAndScore[1] + move[1].getScore()))
				elif move[2] in ('TL', 'LT'):
					# Increases the score of that word by adding twice the letter's value (added thrice in total)
					wordsInRowAndScores[i] = (wordAndScore[0], (wordAndScore[1] + 2 * move[1].getScore()))
				# If it doesn't match, the square type could be a premium square that boosts the word score

	# Corrects score by activating word multipliers
	for move in tilesPlaced:  # Going through stack entries in the move stack
		# Iterate through the index position and tuples in wordsInRowAndScores
		for i, wordAndScore in enumerate(wordsInRowAndScores):
			# Checking if the letter of the tile placed is in the word
			if move[1].getLetter() in wordAndScore[0]:
				# Checking if the square in which the tile was placed is a premium square that boosts word score
				if move[2] in ('DW', 'MD', 'DP'):
					# Doubles the score of the word
					wordsInRowAndScores[i] = (wordAndScore[0], (wordAndScore[1] * 2))
				elif move[2] in ('TW', 'MT', 'TP'):
					# Triples the score of the word
					wordsInRowAndScores[i] = (wordAndScore[0], (wordAndScore[1] * 3))
	'''The 3 for loops below correct the score of vertically formed words'''

	# Corrects score by removing incorrectly added scores from blank tiles
	for move in tilesPlaced:  # Going through stack entries in the move stack
		# Iterate through the index position and tuples in wordsInColumnAndScores
		for i, wordAndScore in enumerate(wordsInColumnAndScores):
			# Checking if the letter of the tile placed is in the word and if the score is 0, which indicates a blank
			if move[1].getLetter() in wordAndScore[0] and move[1].getScore() == 0:
				# Removes the letter's value from the word's score, since a blank tile should award 0 points
				wordsInColumnAndScores[i] = (wordAndScore[0], (wordAndScore[1] - lexicon[move[1].getLetter()][0]))

	# Corrects score by activating letter multipliers
	for move in tilesPlaced:  # Going through stack entries in the move stack
		# Iterate through the index position and tuples in wordsInColumnAndScores
		for i, wordAndScore in enumerate(wordsInColumnAndScores):
			# Checks if the letter of the tile placed is in the word
			if move[1].getLetter() in wordAndScore[0]:
				# Checking if the square in which the tile was placed is a premium square that boosts letter score
				if move[2] in ('DL', 'LD'):
					# Increases the score of that word by adding the letter's value again (added twice in total)
					wordsInColumnAndScores[i] = (wordAndScore[0], (wordAndScore[1] + move[1].getScore()))
				elif move[2] in ('TL', 'LT'):
					# Increases the score of that word by adding twice the letter's value (added thrice in total)
					wordsInColumnAndScores[i] = (wordAndScore[0], (wordAndScore[1] + 2 * move[1].getScore()))
		# If it doesn't match, the square type could be a premium square that boosts the word score

	# Corrects score by activating word multipliers
	for move in tilesPlaced:  # Going through stack entries in the move stack
		# Iterate through the index position and tuples in wordsInColumnAndScores
		for i, wordAndScore in enumerate(wordsInColumnAndScores):
			# Checks if the letter of the tile placed is in the word formed
			if move[1].getLetter() in wordAndScore[0]:
				# Checking if the square in which the tile was placed is a premium square that boosts word score
				if move[2] in ('DW', 'MD', 'DP'):
					# Doubles the score of the word
					wordsInColumnAndScores[i] = (wordAndScore[0], (wordAndScore[1] * 2))
				elif move[2] in ('TW', 'MT', 'TP'):
					# Triples the score of the word
					wordsInColumnAndScores[i] = (wordAndScore[0], (wordAndScore[1] * 3))

	# Adding the score of all the words in wordsInRowAndScores
	for wordAndScore in wordsInRowAndScores:
		score += wordAndScore[1]
	# Adding the score of all the words in wordsInColumnAndScores
	for wordAndScore in wordsInColumnAndScores:
		score += wordAndScore[1]

	return score


# Add information of a move to the GameHistory table of the database
def RecordMoveToGameHistory(gameID, moveNumber, playerID, words, score, exchanged, skipped):
	# Opens an SQL connection to the database
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		# Take the details of the move and create a record of the move in the GameHistory table
		cursor.execute('''INSERT INTO GameHistory 
		('gameID', 'moveNumber', 'playerID', 'words', 'score', 'exchanged', 'skipped') 
		VALUES (?, ?, ?, ?, ?, ?, ?)''', (gameID, moveNumber, playerID, words, score, exchanged, skipped,))


# Apply post-game penalties
def ApplyPenalties(player, scoreStolen, lexicon):
	if player.timer.isOvertime:
		# Remove 10 points for every used minute of the overtime timer
		scoreToRemove = -10 * (10 - player.timer.currentSeconds // 60)  # Get the decreasing value
		player.score.updateScore(scoreToRemove)  # Updates the score

	if not scoreStolen:
		# Decreases the score of a player by the value of their rack
		scoreToRemove = -1 * player.rack.getTotalScore(lexicon)  # Get the decreasing value
		player.score.updateScore(scoreToRemove)  # Updates the score
	return player


# Check if the administrator password entered matches the password of the administrator who is moderating the game
def VerifyAdminPassword(password, IDToUse):
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		# Fetch the password of the administrator moderating the game
		cursor.execute('SELECT password FROM Administrators WHERE adminID=?', (IDToUse,))
		moderatorPassword = cursor.fetchone()[0]
		# Fetch the password of the first administrator, who should be the main host/director
		cursor.execute('SELECT password FROM Administrators WHERE adminID=1')
		topBossPassword = cursor.fetchone()[0]
		if password is None:  # Checks if a password has been entered
			return False
		else:
			# Check if password entered matches the moderator password or the director password
			if password == moderatorPassword or password == topBossPassword:
				return True
			else:
				return False


# Main subroutine to launch the pygame window and run the game
def CreateGameWindow(adminID='1', P1Name='', P2Name='', NewGameLang=None, FileToLoad=None):

	# Starting the pygame window
	pg.init()

	# Setting the window's icon, title, and size
	windowIcon = pg.image.load(os.path.join(os.path.dirname(__file__), '../assets\\images\\EnglishLetters\\TILE_S.png'))
	pg.display.set_icon(windowIcon)
	pg.display.set_caption('Scrabble Tournament Game Hoster')
	GameWindow = pg.display.set_mode((1600, 900))

	# Create background
	Background = pg.Surface((1600, 900))
	Background.fill(pg.Color('#3e231e'))

	# Create UIManager for buttons
	UIManager = pg_gui.UIManager((1600, 900))

	# Creating clock and timer
	clock = pg.time.Clock()
	pg.time.set_timer(pg.USEREVENT, 1000)

	# Flags and Important Variables
	Flags = [True, False, False, True, False, 2, False, False, False, 0, False, False, False, False, False, False,
			False, False, 1]

	if NewGameLang:
		GameBoard, Player1, Player2, TileBag = StartNewGame(NewGameLang, P1Name, P2Name)
	elif FileToLoad:
		GameBoard, TileBag, Player1, Player2, Flags, P1Name, P2Name = LoadGame(FileToLoad)
	else:
		GameBoard, Player1, Player2, TileBag = StartNewGame('English', P1Name, P2Name)

	Player1_ID = GetPlayerID(P1Name)
	Player2_ID = GetPlayerID(P2Name)

	gameID = None

	if NewGameLang is None:
		gameID = GetGameID(FileToLoad)

	# Flags and important variables being assigned
	Player1_Turn = Flags[0]
	OrderDetermined = Flags[1]
	ReadyToStart = Flags[2]
	FirstTurn = Flags[3]
	InvalidPlay = Flags[4]
	BlankTilesInPlay = Flags[5]
	BlankTileDesignationRequired = Flags[6]
	BlankTileSelected = Flags[7]
	ExchangeOccurring = Flags[8]
	ConsecutiveZeroPointPlays = Flags[9]
	ScoresFinalised = Flags[10]
	if FileToLoad and not Flags[13]:
		Paused = True
		# Pause_Button.enable()
	elif FileToLoad:
		Paused = Flags[11]
	else:
		Paused = Flags[11]
	ScoreStolen = Flags[12]
	GameOver = Flags[13]
	RevealOtherRack = Flags[14]
	SpritesAltered = False
	Player1_TileClicked = Flags[15]
	Player2_TileClicked = Flags[16]
	FileNameEntered = Flags[17]
	MoveNumber = Flags[18]
	FileName = ''

	# BUTTONS
	DetermineOrder_Button = pg_gui.elements.UIButton(relative_rect=pg.Rect((84, 725), (100, 50)), text='Pick Tile',
													manager=UIManager)

	ShuffleBag_Button = pg_gui.elements.UIButton(relative_rect=pg.Rect((218, 650), (100, 50)), text='Shuffle',
												manager=UIManager)  # Commented some code in the UIButton class to prevent pygame.USEREVENT usage
	ShuffleBag_Button.disable()

	FillRack_Button = pg_gui.elements.UIButton(relative_rect=pg.Rect((84, 650), (100, 50)), text='Fill Rack',
											manager=UIManager)  # Need to mention ui_button has been edited in the NEA doc
	FillRack_Button.disable()

	SwapTurn_Button = pg_gui.elements.UIButton(relative_rect=pg.Rect((218, 725), (100, 50)), text='Swap',
											manager=UIManager)
	SwapTurn_Button.disable()

	UndoMove_Button = pg_gui.elements.UIButton(relative_rect=pg.Rect((84, 800), (100, 50)), text='Undo Move',
											manager=UIManager)
	UndoMove_Button.disable()

	ExchangeTile_Button = pg_gui.elements.UIButton(relative_rect=pg.Rect((218, 800), (100, 50)), text='Exchange',
												manager=UIManager)
	ExchangeTile_Button.disable()

	Pause_Button = pg_gui.elements.UIButton(relative_rect=pg.Rect((1480, 20), (100, 50)), text='Pause',
											manager=UIManager)
	if FileToLoad is None:
		Pause_Button.disable()
	else:
		Pause_Button.text = 'Resume'
		Pause_Button.rebuild()

	GetAdminPassword_Button = pg_gui.elements.UIButton(relative_rect=pg.Rect((1460, 425), (75, 30)),  text='Enter',
													manager=UIManager, text_kwargs={'size': '4'})
	GetAdminPassword_Button.hide()
	GetAdminPassword_Button.disable()

	GetFileName_Button = pg_gui.elements.UIButton(relative_rect=pg.Rect((1460, 325), (75, 30)), text='Enter',
												manager=UIManager, text_kwargs={'size': '4'})
	GetFileName_Button.hide()
	GetFileName_Button.disable()

	CancelCloseWindow_Button = pg_gui.elements.UIButton(relative_rect=pg.Rect((1300, 475), (100, 50)), text='Cancel',
													manager=UIManager)
	CancelCloseWindow_Button.hide()
	CancelCloseWindow_Button.disable()

	# LABELS & OTHER GUI ITEMS
	AdminPassword_Entry = pg_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pg.Rect((1250, 425), (200, 30)),
																			manager=UIManager)
	AdminPassword_Entry.hide()
	AdminPassword_Entry.disable()

	AdminPassword_Entry_Label = ScrabbleItemTemplates.Text((1252, 400), (200, 50), 'Enter Admin Password:')

	FileName_Entry = pg_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pg.Rect((1250, 325), (200, 30)),
																		manager=UIManager)
	FileName_Entry.hide()
	FileName_Entry.disable()

	FileName_Entry_Label = ScrabbleItemTemplates.Text((1252, 300), (200, 50), 'Enter File Name (min. 6 characters):')

	InvalidPlay_Warning = ScrabbleItemTemplates.Text((1210, 338), (200, 100), 'Invalid Play. Try again.')

	PickLetter_Menu = pg_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=TileBag.alphabet[1:],
																		starting_option='A',
																		relative_rect=pg.Rect((350, 338), (50, 20)),
																		manager=UIManager)
	PickLetter_Menu.hide()

	# Stack to track moves in a play, and list of valid words played
	tilesPlaced = []
	wordsPlayed = [[], []]

	running = True

	while running:

		# Set window to 30FPS
		time_delta = clock.tick(30) / 1000.0

		# If players have picked a tile and determined the order, determineOrder_button is killed & shuffleBag_Button
		# is enabled
		if OrderDetermined:
			if DetermineOrder_Button.is_enabled == 1:
				DetermineOrder_Button.disable()
				DetermineOrder_Button.kill()
				ShuffleBag_Button.enable()

		# If the tile bag has been shuffled, the shuffleBag_button is removed, and fillRack_button & swapTurn_button
		# is enabled
		if TileBag.shuffleCount >= 2:
			if ShuffleBag_Button.is_enabled == 1:
				ShuffleBag_Button.disable()
				ShuffleBag_Button.kill()
			if gameID is None:
				FillRack_Button.enable()

		if BlankTileDesignationRequired and PickLetter_Menu.is_enabled == 0:
			# selectLetterToReplace.show()
			PickLetter_Menu.enable()

		# Going through	all events that occur during each tick
		for event in pg.event.get():

			# If the game has ended
			if ConsecutiveZeroPointPlays == 6 or GameOver:
				RevealOtherRack = True  # So the other player's rack is visible
				InvalidPlay = False

				# Moving the other player's Tiles to another position
				if Player1_Turn and not SpritesAltered:
					Player2.rack.alterSprites()
					SpritesAltered = True
				elif not Player1_Turn and not SpritesAltered:
					Player1.rack.alterSprites()
					SpritesAltered = True

				# If the scores haven't been finalised after the game has ended
				if not ScoresFinalised:
					Player1 = ApplyPenalties(Player1, ScoreStolen, TileBag.lexicon)
					Player2 = ApplyPenalties(Player2, ScoreStolen, TileBag.lexicon)
					ScoresFinalised = True
					if Player1.timer.currentSeconds == 0 and Player1.score.isOvertime:
						scoreDiff = Player1.score.getScore() - Player2.score.getScore()
						if scoreDiff > -1:
							Player2.score.updateScore(scoreDiff+1)
					if Player2.timer.currentSeconds == 0 and Player2.score.isOvertime:
						scoreDiff = Player2.score.getScore() - Player1.score.getScore()
						if scoreDiff > -1:
							Player2.score.updateScore(scoreDiff+1)

				# Checking if a key has been pressed
				if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
					# hide text in the admin password entry
					AdminPassword_Entry.set_text_hidden()

				# Showing the entry to get the file name, and it's label
				if GetFileName_Button.is_enabled == 0:
					GetFileName_Button.show()
					GetFileName_Button.enable()
					FileName_Entry.show()
					FileName_Entry.enable()

				# Showing the entry to get the admin password, and it's label
				if GetAdminPassword_Button.is_enabled == 0:
					GetAdminPassword_Button.show()
					GetAdminPassword_Button.enable()
					AdminPassword_Entry.show()
					AdminPassword_Entry.enable()
					AdminPassword_Entry.set_text_hidden()

				# Disabling buttons
				if SwapTurn_Button.is_enabled == 1:
					# disable
					SwapTurn_Button.disable()

				if ExchangeTile_Button.is_enabled == 1:
					# disable
					ExchangeTile_Button.disable()

				if UndoMove_Button.is_enabled == 1:
					# disable
					UndoMove_Button.disable()

				if Pause_Button.is_enabled == 1:
					# disable
					Pause_Button.disable()

				# Checking for button clicks
				if event.type == pg_gui.UI_BUTTON_PRESSED:
					if event.ui_element == GetAdminPassword_Button:
						# Checking if the entered password matches the password of the person moderating the game, or
						# the top boss of the tournament
						correctPasswordEntered = VerifyAdminPassword(AdminPassword_Entry.get_text(), adminID)
						if correctPasswordEntered:
							running = False
							break

					if event.ui_element == GetFileName_Button:
						FileName = FileName_Entry.get_text()
						if len(FileName) >= 8 and FileName.isalnum():
							FileNameEntered = True

			if event.type == pg.QUIT and ReadyToStart and not GameOver:
				InvalidPlay = False

				if Pause_Button.is_enabled == 1:
					# disable
					Pause_Button.disable()

				if SwapTurn_Button.is_enabled == 1:
					# disable
					SwapTurn_Button.disable()

				if ExchangeTile_Button.is_enabled:
					# disable
					ExchangeTile_Button.disable()

				if UndoMove_Button.is_enabled == 1:
					# disable
					UndoMove_Button.disable()

				if not Paused and not GameOver:
					# pause game
					Paused = True

				if CancelCloseWindow_Button.is_enabled == 0:
					# show
					CancelCloseWindow_Button.show()
					CancelCloseWindow_Button.enable()

				if FileName_Entry.is_enabled == 0:
					# Allow user to save file
					FileName_Entry.show()
					FileName_Entry.enable()
					GetFileName_Button.show()
					GetFileName_Button.enable()

				if AdminPassword_Entry.is_enabled == 0:
					# Allow password input
					AdminPassword_Entry.show()
					AdminPassword_Entry.enable()
					GetAdminPassword_Button.show()
					GetAdminPassword_Button.enable()

			elif event.type == pg.QUIT and not ReadyToStart:
				running = False
				break

			# Checking for button clicks
			if event.type == pg_gui.UI_BUTTON_PRESSED:

				# If admin password has been entered
				if event.ui_element == GetAdminPassword_Button and FileNameEntered:
					# Check if admin password entered matches password of person moderating the game, or password of the
					# top boss of the tournament
					correctPasswordEntered = VerifyAdminPassword(AdminPassword_Entry.get_text(), adminID)
					if correctPasswordEntered:
						running = False
						break

				# If file name has been entered
				if event.ui_element == GetFileName_Button:
					# Get the file name from the entry box
					FileName = FileName_Entry.get_text()
					# Ensure file name is valid and long enough to make sense
					if len(FileName) >= 8 and FileName.isalnum():
						FileNameEntered = True

				# If the closing of the window is cancelled
				if event.ui_element == CancelCloseWindow_Button:
					GetFileName_Button.hide()
					GetFileName_Button.disable()
					FileName_Entry.hide()
					FileName_Entry.disable()
					GetAdminPassword_Button.hide()
					GetAdminPassword_Button.disable()
					AdminPassword_Entry.hide()
					AdminPassword_Entry.disable()
					CancelCloseWindow_Button.hide()
					CancelCloseWindow_Button.disable()
					Pause_Button.enable()
					SwapTurn_Button.enable()
					ExchangeTile_Button.enable()
					UndoMove_Button.enable()
					Paused = False

				# If the game is paused
				if event.ui_element == Pause_Button and not GameOver:
					if not Paused:
						Pause_Button.text = 'Resume'
						Pause_Button.rebuild()
						ExchangeTile_Button.disable()
						SwapTurn_Button.disable()
						UndoMove_Button.disable()
						Paused = True
					else:
						Pause_Button.text = 'Pause'
						Pause_Button.rebuild()
						ExchangeTile_Button.enable()
						SwapTurn_Button.enable()
						UndoMove_Button.enable()
						Paused = False

				# If a player requests for a tile exchange
				if (event.ui_element == ExchangeTile_Button and (Player1_TileClicked or Player2_TileClicked) and not
				(GameOver or Paused)):
					BlankTileSelected = False
					BlankTileDesignationRequired = False
					PickLetter_Menu.hide()
					if Player1_TileClicked:
						Player1, TileBag, Player1_TileClicked = ExchangeTile(Player1, TileBag)
					else:
						Player2, TileBag, Player2_TileClicked = ExchangeTile(Player2, TileBag)
					ExchangeOccurring = True

				# if fillRack_button has been pressed
				if event.ui_element == FillRack_Button and TileBag.shuffleCount >= 2 and not GameOver:
					Player1.rack.fillRack(TileBag)
					Player1.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)
					Player2.rack.fillRack(TileBag)
					Player2.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)
					ReadyToStart = True
					FillRack_Button.disable()
					Pause_Button.enable()
					SwapTurn_Button.enable()
					UndoMove_Button.enable()
					ExchangeTile_Button.enable()
					if NewGameLang is not None:
						gameID = CreateGameRecord(adminID, Player1_ID, Player2_ID)

				# if shuffleBag_button has been pressed
				if event.ui_element == ShuffleBag_Button:
					# Shuffle bag
					TileBag.shuffleBag()

				# If the player wants to recall their tiles
				if event.ui_element == UndoMove_Button and not (GameOver or Paused):
					if Player1_Turn:
						# undo move for Player 1
						GameBoard, tilesPlaced, Player1 = UndoPlay(GameBoard, Player1, TileBag.getLanguage(), tilesPlaced)
					else:
						GameBoard, tilesPlaced, Player2 = UndoPlay(GameBoard, Player2, TileBag.getLanguage(), tilesPlaced)
					BlankTileSelected = False
					PickLetter_Menu.hide()

				# If determineOrder_button has been pressed
				if event.ui_element == DetermineOrder_Button and not GameOver:
					Player1Tile = ''
					Player2Tile = ''

					# Indefinite iterative loop used to ensure players draw a tile different to the other
					while Player1Tile == Player2Tile:
						Player1Tile = DetermineOrder(TileBag)
						Player2Tile = DetermineOrder(TileBag)

					# Checking which tile takes precedence and swaps players accordingly
					if TileBag.alphabet.index(Player1Tile) > TileBag.alphabet.index(Player2Tile):
						Player1, Player2, P1Name, P2Name, Player1_ID, Player2_ID = SwapPlayers(Player1, Player2, P1Name,
																								P2Name, Player1_ID,
																								Player2_ID)
					OrderDetermined = True

				# If the player is swapping their turn
				if event.ui_element == SwapTurn_Button and TileBag.shuffleCount >= 2 and not (GameOver or Paused):
					if not ExchangeOccurring:
						validPlay, wordsFormed = CheckValidPlacement(GameBoard, TileBag.alphabet, tilesPlaced,
																	FirstTurn)
						if validPlay and wordsFormed:
							wordsCreated, AllWordsOnBoard = CollectWordsPlayed(GameBoard, TileBag.alphabet, TileBag.getLanguage(),
															wordsPlayed)
							validPlay = CheckWords(wordsCreated, TileBag.getLanguage())
							if validPlay:
								score = CalculateScore(wordsCreated, tilesPlaced, TileBag.lexicon)
								Player1_Turn = not Player1_Turn
								FirstTurn = False
								if Player1_Turn:
									if not TileBag.isEmpty():
										if len(tilesPlaced) == 7:
											score += 50
										Player2.rack.fillRack(TileBag)
										Player2.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)
										Player2.score.updateScore(score)

									else:
										if Player2.rack.isEmpty():
											scoreToSteal = Player1.rack.getTotalScore(TileBag.lexicon)
											Player2.score.updateScore(scoreToSteal * 2)
											GameOver = True
											ScoreStolen = True
								else:
									if not TileBag.isEmpty():
										if len(tilesPlaced) == 7:
											score += 50
										Player1.rack.fillRack(TileBag)
										Player1.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)
										Player1.score.updateScore(score)
									else:
										if Player1.rack.isEmpty():
											scoreToSteal = Player2.rack.getTotalScore(TileBag.lexicon)
											Player1.score.updateScore(scoreToSteal * 2)
											GameOver = True
											ScoreStolen = True
								InvalidPlay = False
								wordsCreatedString = ','.join(wordsCreated[0]) + ',' + ','.join(wordsCreated[1])
								if Player1_Turn:
									RecordMoveToGameHistory(gameID, MoveNumber, Player2_ID, wordsCreatedString, score,
															False, False)
								else:
									RecordMoveToGameHistory(gameID, MoveNumber, Player1_ID, wordsCreatedString, score,
															False, False)
								if BlankTilesInPlay == 0:
									PickLetter_Menu.kill()
								else:
									PickLetter_Menu.disable()
									PickLetter_Menu.hide()
								MoveNumber += 1
								tilesPlaced = []
								for i, row in enumerate(wordsCreated):
									for word in row:
										wordsPlayed[i].append(word)
								ConsecutiveZeroPointPlays = 0

							else:
								if Player1_Turn:
									GameBoard, tilesPlaced, Player1 = UndoPlay(GameBoard, Player1,
																			TileBag.getLanguage(), tilesPlaced)
								else:
									GameBoard, tilesPlaced, Player2 = UndoPlay(GameBoard, Player2,
																			TileBag.getLanguage(), tilesPlaced)
								InvalidPlay = True
						elif validPlay and len(tilesPlaced) == 0:
							Player1_Turn = not Player1_Turn
							if Player1_Turn:
								RecordMoveToGameHistory(gameID, MoveNumber, Player2_ID, '', 0, False, True)
							else:
								RecordMoveToGameHistory(gameID, MoveNumber, Player1_ID, '', 0, False, True)
							MoveNumber += 1
							ConsecutiveZeroPointPlays += 1
						else:
							if Player1_Turn:
								GameBoard, tilesPlaced, Player1 = UndoPlay(GameBoard, Player1,
																			TileBag.getLanguage(), tilesPlaced)
							else:
								GameBoard, tilesPlaced, Player2 = UndoPlay(GameBoard, Player2,
																			TileBag.getLanguage(), tilesPlaced)
							InvalidPlay = True
					else:
						Player1_Turn = not Player1_Turn
						if Player1_Turn:
							sprites = Player2.rack.getSprites()
							for i in range(7):
								if sprites[f'TILE{i + 1}'] is not None:
									sprites[f'TILE{i + 1}'].canBeClicked = True
									sprites[f'TILE{i + 1}'].updateImage(
										f"{TileBag.getLanguage()}Letters\\TILE_{Player2.rack.getContents()[i]}.png")
							Player2.rack.updateSprites(sprites)
							RecordMoveToGameHistory(gameID, MoveNumber, Player2_ID, '', 0,
													ExchangeOccurring, False)
						else:
							sprites = Player1.rack.getSprites()
							for i in range(7):
								if sprites[f'TILE{i + 1}']:
									sprites[f'TILE{i + 1}'].canBeClicked = True
									sprites[f'TILE{i + 1}'].updateImage(
										f"{TileBag.getLanguage()}Letters\\TILE_{Player1.rack.getContents()[i]}.png")
							Player1.rack.updateSprites(sprites)
							RecordMoveToGameHistory(gameID, MoveNumber, Player1_ID, '', 0,
													ExchangeOccurring, False)
						ConsecutiveZeroPointPlays += 1
						MoveNumber += 1
						ExchangeOccurring = False

			# Used to decrement the timer
			if event.type == pg.USEREVENT and ReadyToStart and not (GameOver or Paused):
				if Player1.timer.currentSeconds != 0 and Player1_Turn and not GameOver:
					Player1.timer.currentSeconds -= 1
					if not Player1.timer.isOvertime:
						Player1.timer.updateTimer()
					else:
						Player1.timer.updateOvertimeTimer()
					if ConsecutiveZeroPointPlays == 6:
						GameOver = True
					if Player1.timer.currentSeconds == 0 and not Player1.timer.isOvertime and not GameOver:
						Player1.replaceTimer()
					elif Player1.timer.currentSeconds == 0 and Player1.timer.isOvertime:
						GameOver = True

				if Player2.timer.currentSeconds != 0 and not Player1_Turn and not GameOver:
					Player2.timer.currentSeconds -= 1
					if not Player2.timer.isOvertime:
						Player2.timer.updateTimer()
					else:
						Player2.timer.updateOvertimeTimer()
					if ConsecutiveZeroPointPlays == 6:
						GameOver = True
					if Player2.timer.currentSeconds == 0 and not Player2.timer.isOvertime and not GameOver:
						Player2.replaceTimer()
					elif Player2.timer.currentSeconds == 0 and Player2.timer.isOvertime:
						GameOver = True

			# If a letter has been selected for the blank tile
			if event.type == pg_gui.UI_DROP_DOWN_MENU_CHANGED and not Paused:
				if event.ui_element == PickLetter_Menu:
					# Update the blank tile accordingly
					GameBoard, tilesPlaced, BlankTileSelected = DesignateBlank(GameBoard, tilesPlaced,
																			TileBag.getLanguage(), event.text)
					PickLetter_Menu.disable()
					PickLetter_Menu.hide()
					BlankTilesInPlay -= 1
					BlankTileSelected = False
					BlankTileDesignationRequired = False

			# if the left mouse button has been clicked
			if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0] and not (GameOver or Paused):
				mouse_pos = pg.mouse.get_pos()  # Get the coordinates of the mouse click

				# Used to check if the mouse click was within the rack AND if a tile hasn't been selected for Player 1
				if (Player1_Turn and not Player1_TileClicked and (584 <= mouse_pos[0] <= 1016) and
					(798 <= mouse_pos[1] <= 846) and not BlankTileSelected):
					Player1_TileClicked, BlankTileSelected = SelectTile(Player1, mouse_pos)
					if not BlankTileSelected:
						PickLetter_Menu.disable()
					if BlankTileSelected and not ExchangeOccurring:
						PickLetter_Menu.show()
						PickLetter_Menu.disable()

				# Used to check if the mouse click was within the board AND if a tile has been selected for Player 1
				elif (Player1_Turn and Player1_TileClicked and (448 <= mouse_pos[0] <= 1152) and
					(58 <= mouse_pos[1] <= 762) and not ExchangeOccurring):
					row, column = SelectSquare(GameBoard, mouse_pos)
					if not (row == -1 and column == -1):
						Player1_TileClicked, tilesPlaced = GetSelectedTile(Player1, tilesPlaced)
						GameBoard, tilesPlaced = PlaceTile(GameBoard, row, column, tilesPlaced)
						if BlankTileSelected:
							BlankTileDesignationRequired = True

				# Used to check if the mouse click was within the rack AND if a tile hasn't been selected for Player 2
				elif (not Player1_Turn and not Player2_TileClicked and (584 <= mouse_pos[0] <= 1016) and
					(798 <= mouse_pos[1] <= 846) and not BlankTileSelected):
					Player2_TileClicked, BlankTileSelected = SelectTile(Player2, mouse_pos)
					if BlankTileSelected and not ExchangeOccurring:
						PickLetter_Menu.show()
						PickLetter_Menu.disable()

				# Used to check if the mouse click was within the board AND if a tile has been selected for Player 2
				elif (not Player1_Turn and Player2_TileClicked and (448 <= mouse_pos[0] <= 1152) and
					(58 <= mouse_pos[1] <= 762) and not ExchangeOccurring):
					row, column = SelectSquare(GameBoard, mouse_pos)
					if not (row == -1 and column == -1):
						Player2_TileClicked, tilesPlaced = GetSelectedTile(Player2, tilesPlaced)
						GameBoard, tilesPlaced = PlaceTile(GameBoard, row, column, tilesPlaced)
						if BlankTileSelected:
							BlankTileDesignationRequired = True

			if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
				if AdminPassword_Entry.is_enabled == 1:
					AdminPassword_Entry.set_text_hidden()

			# Processing anything pygame_gui related for the event
			try:
				UIManager.process_events(event)
			except IndexError:
				AdminPassword_Entry.clear()

		# Update game window, draw background, and draw buttons
		UIManager.update(time_delta)
		GameWindow.blit(Background, (0, 0))
		UIManager.draw_ui(GameWindow)

		# Blit the board and tile bag
		GameWindow.blit(GameBoard.getImage(), (GameBoard.getRectCoordinates()))
		GameWindow.blit(TileBag.getImage(), (TileBag.getRectCoordinates()))

		# Blit the rack and tiles for whose turn it is
		if Player1_Turn and not GameOver:
			GameWindow.blit(Player1.rack.getImage(), (Player1.rack.getRectCoordinates()))
			GameWindow.blit(ScrabbleItemTemplates.Text((568, 875), (200, 100),
														f'{Player1.name} - Player 1').text,
							(568, 875))
			# Player1.rack.drawGroup(gameWindow)
			Player1.rack.getGroup().draw(GameWindow)
		elif not Player1_Turn and not GameOver:

			GameWindow.blit(Player2.rack.getImage(), (Player2.rack.getRectCoordinates()))
			GameWindow.blit(ScrabbleItemTemplates.Text((568, 875), (200, 100),
														f'{Player2.name} - Player 2').text,
							(568, 875))
			# Player2.rack.drawGroup(gameWindow)
			Player2.rack.getGroup().draw(GameWindow)

		# Blit the score and timer for both players
		GameWindow.blit(Player1.timer.text, Player1.timer.getRectCoordinates())
		GameWindow.blit(Player1.score.text, Player1.score.getRectCoordinates())

		GameWindow.blit(Player2.timer.text, Player2.timer.getRectCoordinates())
		GameWindow.blit(Player2.score.text, Player2.score.getRectCoordinates())

		# If the game is over and the other player's rack needs to be shown, the rack and player label will be moved
		if RevealOtherRack and Player1_Turn:
			GameWindow.blit(Player2.rack.getImage(), (1050, 775))
			GameWindow.blit(ScrabbleItemTemplates.Text((1068, 875), (200, 100),
														f'{Player2.name} - Player 2').text, (1068, 875))
			GameWindow.blit(ScrabbleItemTemplates.Text((568, 875), (200, 100),
														f'{Player1.name} - Player 1').text, (568, 875))
			Player2.rack.getGroup().draw(GameWindow)
			GameWindow.blit(Player1.rack.getImage(), Player1.rack.getRectCoordinates())
			Player1.rack.getGroup().draw(GameWindow)
		elif RevealOtherRack and not Player1_Turn:
			GameWindow.blit(Player1.rack.getImage(), (1050, 775))
			GameWindow.blit(
				ScrabbleItemTemplates.Text((1068, 875), (200, 100),
											f'{Player1.name} - Player 1').text, (1068, 875))
			GameWindow.blit(ScrabbleItemTemplates.Text((568, 875), (200, 100),
														f'{Player2.name} - Player 2').text, (568, 875))
			Player1.rack.getGroup().draw(GameWindow)
			GameWindow.blit(Player2.rack.getImage(), Player2.rack.getRectCoordinates())
			Player2.rack.getGroup().draw(GameWindow)

		if GetFileName_Button.is_enabled == 1:
			# Show label
			GameWindow.blit(FileName_Entry_Label.text, FileName_Entry_Label.rect)
		if GetAdminPassword_Button.is_enabled == 1:
			# Show label
			GameWindow.blit(AdminPassword_Entry_Label.text, AdminPassword_Entry_Label.rect)

		if InvalidPlay:
			# Show warning
			GameWindow.blit(InvalidPlay_Warning.text, (InvalidPlay_Warning.rect.x, InvalidPlay_Warning.rect.y))

		for row in GameBoard.squares:
			for square in row:
				if isinstance(square, ScrabbleItemTemplates.Square):
					x, y = square.getRectCoordinates()
					GameWindow.blit(square.getText(), (x + 2, y + 6))

		GameBoard.getGroup().draw(GameWindow)

		pg.display.update()

	pg.quit()

	boardDict = {
		'1': GameBoard.getBoard()[0],
		'2': GameBoard.getBoard()[1],
		'3': GameBoard.getBoard()[2],
		'4': GameBoard.getBoard()[3],
		'5': GameBoard.getBoard()[4],
		'6': GameBoard.getBoard()[5],
		'7': GameBoard.getBoard()[6],
		'8': GameBoard.getBoard()[7],
		'9': GameBoard.getBoard()[8],
		'10': GameBoard.getBoard()[9],
		'11': GameBoard.getBoard()[10],
		'12': GameBoard.getBoard()[11],
		'13': GameBoard.getBoard()[12],
		'14': GameBoard.getBoard()[13],
		'15': GameBoard.getBoard()[14]
	}

	tileBagDict = {
		'Bag': TileBag.bag,
		'Language': TileBag.getLanguage()
	}

	Player1Dict = {
		'Name': Player1.name,
		'Rack': Player1.rack.getContents(),
		'Score': Player1.score.getScore(),
		'Timer': {
			'Time Left': Player1.timer.currentSeconds,
			'Overtime': Player1.timer.isOvertime
		}

	}

	Player2Dict = {
		'Name': Player2.name,
		'Rack': Player2.rack.getContents(),
		'Score': Player2.score.getScore(),
		'Timer': {
			'Time Left': Player2.timer.currentSeconds,
			'Overtime': Player2.timer.isOvertime
		}
	}

	flagsDict = {
		"Player1_Turn": Player1_Turn,
		"OrderDetermined": OrderDetermined,
		"ReadyToStart": ReadyToStart,
		"FirstTurn": FirstTurn,
		"InvalidPlay": InvalidPlay,
		"BlankTilesInPlay": BlankTilesInPlay,
		"BlankTileDesignationRequired": BlankTileDesignationRequired,
		"BlankTileSelected": BlankTileSelected,
		"ExchangeOccurring": ExchangeOccurring,
		"ConsecutiveZeroPointPlays": ConsecutiveZeroPointPlays,
		"ScoresFinalised": ScoresFinalised,
		"Paused": Paused,
		"ScoreStolen": ScoreStolen,
		"GameOver": GameOver,
		"RevealOtherRack": RevealOtherRack,
		"Player1_TileClicked": Player1_TileClicked,
		"Player2_TileClicked": Player2_TileClicked,
		"FileNameEntered": FileNameEntered,
		"MoveNumber": MoveNumber
	}

	gameDict = {
		'Board': boardDict,
		'Tile Bag': tileBagDict,
		'Player 1': Player1Dict,
		'Player 2': Player2Dict,
		'Flags': flagsDict
	}

	if GameOver:
		if Player1Dict['Score'] > Player2Dict['Score']:
			# Assign Player 1 as winner
			winner = f"Winner: {Player1Dict['Name']}"
		elif Player2Dict['Score'] > Player1Dict['Score']:
			# Assign Player 2 as winner
			winner = f"Winner: {Player2Dict['Name']}"
		else:
			# update to reflect it's a tie
			winner = 'Tie'
	else:
		# Keep winner empty since the game is ongoing
		winner = ''

	try:
		with open(os.path.join(os.path.dirname(__file__), f'../data\\{FileName}.json'), 'w') as f:
			# write gameInfo to file
			json.dump(gameDict, f, indent=4)
	except FileNotFoundError:
		with open(os.path.join(os.path.dirname(__file__), '../data\\GameData.json')) as f:
			# Take current info
			data = json.load(f)
		FileName = f'Game{len(data)}'
		with open(os.path.join(os.path.dirname(__file__), f'../data\\{FileName}.json'), 'w') as f:
			# write gameInfo to file
			json.dump(gameDict, f, indent=4)

	with open(os.path.join(os.path.dirname(__file__), '../data\\GameData.json')) as f:
		# Take current info
		data = json.load(f)

	data[f'{FileName}'] = winner

	with open(os.path.join(os.path.dirname(__file__), '../data\\GameData.json'), 'w') as f:
		# write updated info
		json.dump(data, f, indent=4)

	# Open connection to SQL database and update the game record
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		cursor.execute('''UPDATE Games SET fileName=?, result=? WHERE gameID=?''',
						(FileName, winner, gameID,))
