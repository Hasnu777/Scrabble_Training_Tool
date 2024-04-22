import pygame as pg
import json
import pygame_gui as py_gui
import random
import sqlite3 as sql
import os
from gameLogic import ScrabbleItemTemplatesV2
from datetime import datetime
from CTkMessagebox import CTkMessagebox


# Creates the Scrabble objects
def initialiseScrabbleItems(language, P1Name, P2Name):

	# Creates the gameBoard
	gameBoard = ScrabbleItemTemplatesV2.Board((400, 10))
	# Adds the premium squares to the board
	gameBoard = AddSpecialLocations(gameBoard, language)

	# Creates Player1
	Player1 = ScrabbleItemTemplatesV2.Player(P1Name, (550, 775), (1180, 750), (1180, 720))

	# Creates Player2
	Player2 = ScrabbleItemTemplatesV2.Player(P2Name, (550, 775), (1180, 75), (1180, 45))

	# Creates the Tile Bag
	TileBag = ScrabbleItemTemplatesV2.TileBag((50, 250), language)

	return gameBoard, Player1, Player2, TileBag


# Adds the Square objects onto the board to represent the squares, including premium squares
def AddSpecialLocations(board, language):
	for bonusType in ScrabbleItemTemplatesV2.SpecialLocations.keys():  # Goes through each type of premium square
		for position in ScrabbleItemTemplatesV2.SpecialLocations[bonusType]:  # Goes through each coordinate pair
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
				case _:  # the keys for ScrabbleItemTemplatesV2.SpecialLocations is the English version, hence pass
					pass
			board.addToBoard(position[0], position[1], bonusType)  # Adds the premium square type to the board
			# Creates a Square object and adds it to the board
			board.squares[position[0]][position[1]] = ScrabbleItemTemplatesV2.Square(
				((448 + position[1] * 48), (58 + position[0] * 48)), text=bonusType)
	return board


# Gets the square that has been clicked on by the user
def selectSquare(board, mouse_pos):
	# Below variables are set to -1 to represent a square not being selected, if the for loop doesn't alter them
	row = -1
	column = -1
	for i in range(15):
		for j in range(15):  # The two for loops are used to go through each row and column in the board
			try:
				# Type declaration used to force the below if statement to trigger only if a Square object is fetched
				square: ScrabbleItemTemplatesV2.Square = board.squares[i][j]
				# Checks if user clicked on this Square. .collidepoint(coordinates) is used to see if the coordinates
				# fall within the rect of the Sprite() object.
				if square.getSquareRect().collidepoint(mouse_pos):
					# If it has, then it retrieves the position of the Square relative to the board
					row = i
					column = j
			except AttributeError:  # If a Square object isn't fetched this exception occurs
				continue
	return row, column


# Gets a random tile out of the tile bag
def pickTile(tileBag):
	item = random.choice(tileBag.bag[:-1])  # Picks a random letter. Omits the isEmpty() flag from the bag
	# indexPosition = tileBag.bag.index(item)  # Gets the index position of the selected letter
	# letter = tileBag.bag[indexPosition][0]
	letter = item[0]
	return letter


# Used to swap Player attributes
def swapPlayers(player1, player2):
	# player1.name, player2.name = player2.name, player1.name  # Swaps the names around
	# player1.rack, player2.rack = player2.rack, player1.rack  # Swaps the racks around
	# player1.timer, player2.timer = player2.timer, player1.timer  # Swaps the timers around
	# player1.score, player2.score = player2.score, player1.score  # Swaps the scores around
	return player2, player1


# Used to get the tile clicked by a player from their rack, if a player has clicked on a tile
def selectTile(player, mouse_pos):
	# Used to go through the index position and the Tile object stored in the sprites dictionary of the player
	for i, tile in enumerate(player.rack.getSprites().values()):
		print(i, 'count')
		if tile is not None:  # Used to check if a tile was actually retrieved
			# Used to check if the mouse has clicked on a tile, rather than just the rack. .collidepoint(coordinates)
			# is used to see if the coordinates fall within the rect of the Sprite() object.
			if tile.getRect().collidepoint(mouse_pos):
				print(tile.getLetter(), i, 'tile letter')
				print(tile.canBeClicked, 'tile can be clicked')
				if tile.canBeClicked:  # Checks if the tile is allowed to be placed on the board
					tile.isClicked = True
					if tile.getLetter() == '!':  # Checks if the tile selected is a blank tile
						return True, True  # True for a tile being clicked, True for blankTileClicked
					else:
						return True, False  # True for a tile being clicked, False for blankTileClicked
				else:
					return False, False  # False for both, since a tile hasn't been clicked
	# If the player's rack is completely empty, the if statement is never executed, hence the below return
	return False, False  # False for both, since a tile hasn't been clicked


# Used to retrieve the tile that needs to be moved from the rack to the board
def getTileToMove(player, stack):
	# Iterates through the index positions and tiles in the sprites dictionary for the player's rack
	for i, tile in enumerate(player.rack.getSprites().values()):
		if tile is not None:  # Checks if the tile variable holds a Tile object
			if tile.isClicked:  # Checks if the tile has been clicked
				tile.isClicked = False
				player.rack.removeFromRack(i, tile)  # Takes the tile out of the rack
				# Appends a tuple of the tile's rack position and the tile object to the move stack
				stack.append((i, tile))
				return False, tile, stack


# Used to move the selected tile to the board
def moveTile(board, row, column, tile, stack):
	specialLocation = board.CheckForSpecialLocation(row, column)  # Retrieves square type information from the board
	board.addToBoard(row, column, tile.getLetter())  # Replaces square at the specified board position with the letter
	square = board.squares[row][column]  # Takes square object from the sprites array of the board
	tile.updateRect(square.getRectCoordinates())  # Updates the tile's rect to the coordinates of the square's rect
	tile.transformImage((32, 32))  # Resizes image to 32x32
	tile.isClicked = False
	board.squares[row][column] = tile  # Puts tile sprite into the board's sprites array
	board.addToGroup(tile)  # Adds tile to board Group
	# Creates a stack entry containing: rack position, tile object, square type, square object, board row, board column
	stack[-1] = (stack[-1][0], stack[-1][1], specialLocation, square, row, column)
	return board, specialLocation, stack


# Used to check if the tiles are placed in a valid manner, and retrieves the words played. Valid placement includes: a
# single string of tiles is played (same row/column), a tile is placed on the center square (if first turn), the string
# of tiles placed connects to tiles that have already been played on the board.
def checkTurn(gameBoard, stack, language, alphabet, firstTurn, wordsPlayed):
	validPlay = False

	rowsAndColumns = [(move[4], move[5]) for move in stack]  # Takes the row and column of each newly placed tile
	rows = [move[4] for move in stack]  # takes the row of each newly placed tile
	columns = [move[5] for move in stack]  # Takes the column of each newly placed tile

	if len(rowsAndColumns) > 0:  # Checks if tiles have been placed, shown by rows and columns being retrieved
		# Checks if all rows are the same, or all columns are the same. Done to see if tiles are placed in one string.
		if not (rows.count(rows[0]) == len(rows) or columns.count(columns[0]) == len(columns)):
			return False, [[], []]  # Returns False for validPlay, and an empty list to show no words were retrieved
	else:
		return True, [[], []]  # Returns True for validPlay, and an empty list to show no words were retrieved
		# True is returned because this shows that the user has skipped their turn & not made any moves

	board = gameBoard.getBoard()  # Gets the board

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
		if wordsOnBoard[0].count(word) > wordsPlayed[0].count(word):
			# For loop to add that word the amount of times the word has been created
			for i in range(wordsOnBoard[0].count(word)-wordsPlayed[0].count(word)):
				wordsCreated[0].append(word)

	# Going through words made vertically
	for word in wordsOnBoard[1]:
		# If a word in wordsOnBoard[1] exists more times than in wordsPlayed, it's a newly created word.
		if wordsOnBoard[1].count(word) > wordsPlayed[1].count(word):
			# For loop to add that word the amount of times the word has been created
			for i in range(wordsOnBoard[1].count(word)-wordsPlayed[1].count(word)):
				wordsCreated[1].append(word)

	print(wordsCreated, 'wordsCreated')

	# Checks if the first turn has been made
	if firstTurn:
		# Checks if words have been placed on the board
		if not (len(wordsCreated[0]) == 0 and len(wordsCreated[1]) == 0):
			print('tis the first turn')
			for move in stack:  # Goes through information in the move stack for each tile placed
				print(move[1].getRectCoordinates(), 'rect coords')
				# Boolean value assigned to validPlay to see if a tile has been placed on the center square.
				validPlay = (move[1].getRectCoordinates() == (784, 394))
				print(validPlay, 'for tile on center square')
				if validPlay:
					print('tile detected on center square')
					break  # if a tile has been placed, then the for loop doesn't need to check the other tiles

			if not validPlay:  # Triggers if a tile hasn't been placed on the center square
				print('no tile detected on center square')
				print(validPlay, 'for valid play now')
				return validPlay, [[], []]  # returns False for validPlay and an empty list, since words placed don't matter
		else:  # Triggers if no tiles were placed
			validPlay = True  # If the player has placed no tiles, they're skipping their turn.
	else:
		for move in stack:  # Goes through information in the move stack for each tile placed
			# If statements below will check the squares on either side & above/below the tile placed, to see if there
			# is a tile that connects to the tile. It then checks if the row and column of that connecting tile isn't in
			# rowsAndColumns, because this means that the connecting tile was not newly placed. Hence, the string of
			# tiles is placed in a valid manner. Has an outer if statement to ensure that the altered index position is
			# within the range of the board's rows/columns
			if move[4] - 1 >= 0:  # Checks if the altered row is within bounds
				squareToCheck = board[move[4] - 1][move[5]]  # To get the square to the left
				if squareToCheck in alphabet and (move[4]-1, move[5]) not in rowsAndColumns:
					validPlay = True
					break
			if move[5] - 1 >= 0:  # Checks if the altered column is within bounds
				squareToCheck = board[move[4]][move[5] - 1]  # To get the square below
				if squareToCheck in alphabet and (move[4], (move[5]-1)) not in rowsAndColumns:
					validPlay = True
					break
			if move[4] + 1 <= 14:  # Checks if the altered row is within bounds
				squareToCheck = board[move[4] + 1][move[5]]  # To get the square to the right
				if squareToCheck in alphabet and (move[4]+1, move[5]) not in rowsAndColumns:
					validPlay = True
					break
			if move[5] + 1 <= 14:  # Checks if the altered column is within bounds
				squareToCheck = board[move[4]][move[5] + 1]  # To get the square above
				if squareToCheck in alphabet and (move[4], (move[5]+1)) not in rowsAndColumns:
					validPlay = True
					break

	return validPlay, wordsCreated  # Returns True for validPlay, and the words created


# Undoes the play made by the player by recalling tiles and replacing the squares on the board
def undoPlay(board, stack, Player1_Turn, Player1, Player2, language):
	if not stack:  # If the stack is empty, there's nothing to do
		return board, stack, Player1, Player2
	else:
		rackPosition, tile, squareType, square, row, column = stack.pop()  # Gets info out of the last stack entry
		board.removeFromGroup(tile)  # Removes the tile from the board
		board.squares[row][column] = square  # Adds the square back to the board's sprites array
		tile.updateRect((584+rackPosition*64, 798))  # Moves the tile back to it's place in the rack
		if tile.getScore() == 0:  # Checks if the score of the tile is 0, as this means it is a blank tile
			tile.updateLetter('!')  # Change the letter attribute of the tile back to an exclamation mark
			tile.updateImage(f'FrenchLetters\\TILE_!.png')  # Changes the image back to the blank tile image
		else:  # Triggers if the tile isn't a blank tile
			# Re-loads the image of the tile at the default size
			# Using this instead of transformImage() to avoid unwanted deformation when enlarging the image.
			tile.updateImage(f'{language}Letters\\TILE_{tile.getLetter()}.png')
		board.getBoard()[row][column] = squareType  # Updates the board array to hold the square type
		if Player1_Turn:  # Checks if Player1 made the play
			Player1.rack.addToRack(rackPosition, tile)  # Adds the tile to Player1's rack at the selected rack position
		else:  # Triggers if player 2 made the play
			Player2.rack.addToRack(rackPosition, tile)  # Adds the tile to Player2's rack at the selected rack position
		# Below line is used to call the subroutine again, making it recursive. Recursion is used to undo all tile
		# placements made by the player. This ends up returning board, stack, Player1, Player2 after undoing the first
		# tile placement, which is the first stack entry. It is dealt with last because .pop() takes out items from the
		# end of the array to the front.
		return undoPlay(board, stack, Player1_Turn, Player1, Player2, language)


# def undoMove(board, stack, PlayerTurn, Player1, Player2):
# 	if not stack:
# 		return board, stack, Player1, Player2
# 	rackPosition, tile, squareType, square, row, column = stack.pop()  # (rackPosition, tile, squareType, square, row, column)
# 	board.removeFromGroup(tile)
# 	board.squares[row][column] = square
# 	tile.updateRect((584 + rackPosition * 64, 798))
# 	tile.transformImage((48, 48))
# 	board.getBoard()[row][column] = squareType
# 	if PlayerTurn:
# 		Player1.rack.addToRack(rackPosition, tile)
# 	else:
# 		Player2.rack.addToRack(rackPosition, tile)
# 	return board, stack, Player1, Player2


# Goes through all the newly created words and checks if it is inside the game's dictionary
def checkWords(wordsToCheck, language):
	# Opening a connection to the SQL database, to access the word tables
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		# Used to go through the array of horizontally made words, and the vertically made words
		for row in wordsToCheck:
			for word in row:  # For loop to go through each word
				print(word)
				# Fetches the word from the word table
				cursor.execute(f'SELECT words FROM {language}Words WHERE words=?', (word,))
				wordFetched = cursor.fetchone()
				print(wordFetched)
				if wordFetched is None:  # Checks if a word was actually fetched
					return False
				# if word != wordFetched[0]: UNSURE IF THIS IS NEEDED HONESTLY
				# 	return False
	return True


# Swaps the blank tile image and letter to the letter it's been designated
def swapBlankToLetter(stack, letter, language, gameboard):
	moveMade = stack[-1]  # Takes the stack information
	tile = moveMade[1]  # Takes the Tile object
	gameboard.removeFromGroup(tile)  # Removes the tile from the board's group
	tile.updateLetter(letter)  # Changing the letter
	tile.updateImage(f'{language}Letters\\TILE_{letter}_BLANK.png')  # Updating the image
	tile.transformImage((32, 32))  # Shrinking the image to fit in the board's squares
	gameboard.getBoard()[moveMade[-2]][moveMade[-1]] = tile.getLetter()  # Putting the letter in the board
	gameboard.addToGroup(tile)  # Adding the tile back to the board group
	# Re-creating the stack entry with the updated Tile object
	moveMade = (moveMade[0], tile, moveMade[2], moveMade[3], moveMade[4], moveMade[5])
	stack[-1] = moveMade  # Putting the stack entry inside the stack
	return stack, False, gameboard


# Used to select the tile to exchange
def findTileToExchange(player, tileBag):
	# Iterates through the rack positions and values in the sprites array
	for i, tile in enumerate(player.rack.getSprites().values()):
		print(i, 'find exchange tile count')
		if tile is not None:  # Checks if a Tile object has been revealed
			print(tile.getLetter(), i, 'tile being exchanged')
			print(tile.isClicked, 'tile can be clicked')
			if tile.isClicked:  # Checks if the tile has been clicked
				return exchangeTile(player, tile, i, tileBag)


# Exchange the selected tile with a random tile from the bag
def exchangeTile(player, tileToExchange, tileToExchangePosition, tileBag):
	player.rack.removeFromRack(tileToExchangePosition, tileToExchange)  # Remove the tile from the player's rack
	print(player.rack.getContents())
	letterToExchange = tileToExchange.getLetter()  # Get the letter of the tile being exchanged
	# Flags to hold information of the new tile and it's location
	newTileInfo = None
	newTileInfoPosition = -1
	print(tileBag.bag)
	for i, tile in enumerate(tileBag.bag):  # Iterates through the index positions and tiles in the tile bag
		print(i, 'count for finding letter to put exchanging tile back inside tilebag')
		print(tile[0])
		# Checks if the tile selected from the bag is the same as the letter as the tile being exchanged
		if letterToExchange == tile[0]:
			newTileInfo = (tile[0], tile[1], (tile[2]+1))  # Returns the letter by incrementing the quantity
			newTileInfoPosition = i  # Takes the letter's index position in the tile bag
			print(newTileInfo, newTileInfoPosition, 'new letter info and its position in tile bag')
			break  # Stop the for loop, since the letter has been found
	# If the quantity of this letter was previously 0, it is now 1. The isEmpty() flag needs to be decremented to show
	# that a tile for this letter is available in the tile bag now.
	if newTileInfo[2] == 1:
		tileBag.bag[-1] += 1
	print(tileBag.bag[newTileInfoPosition])
	tileBag.bag[newTileInfoPosition] = newTileInfo  # Puts the letter information back in the tile bag
	player.rack.fillRack(tileBag)  # Fill the player's rack with new tiles
	player.rack.fillRackGroup(tileBag.getLanguage(), tileBag.lexicon)  # Fill the player's rack group with Tile objects
	spritesList = player.rack.getSprites()  # Get the sprites dictionary of the player's rack
	newTile = spritesList[f'TILE{tileToExchangePosition+1}']  # Get the new tile from the exchange
	print(newTile.getLetter(), 'newTile that was put into rack')
	newTile.canBeClicked = False  # Prevents the tile from being exchanged a second time
	newTile.updateImage('TILE_UNKNOWN.png')  # Updates the tile's image to hide the letter from the user.
	# The above is down because the actual rules dictate all tiles to exchange are placed facedown, then you take out
	# all the new tiles, and finally you put the old tiles back in the tile bag. Hiding the letter of the new tile is
	# done to emulate this.
	spritesList[f'TILE{tileToExchangePosition+1}'] = newTile  # Puts the tile back into the sprites dictionary
	player.rack.updateSprites(spritesList)  # Updates the sprites dictionary of the player's rack
	return player, tileBag, False


# Check if the administrator password entered matches the password of the administrator who is moderating the game
def verifyAdminPassword(password, IDToUse):
	with sql.connect(os.path.join(os.path.dirname(__file__), '../scrabbleTrainingTool.db')) as conn:
		cursor = conn.cursor()
		# Fetch the password of the administrator moderating the game
		cursor.execute('SELECT password FROM users WHERE id=?', (IDToUse,))
		moderatorPassword = cursor.fetchone()[0]
		# Fetch the password of the first administrator, who should be the main host/director
		cursor.execute('SELECT password FROM users WHERE id=1')
		topBossPassword = cursor.fetchone()[0]
		print(moderatorPassword, 'mod pwd')
		print(topBossPassword, 'topBoss pwd')
		if password is None:  # Checks if a password has been entered
			return False
		else:
			# Check if password entered matches the moderator password or the director password
			if password == moderatorPassword or password == topBossPassword:
				return True
			else:
				return False


# Calculate the score of all the words formed from a play
def calculateScore(wordsCreated, movesMade, lexicon):  # (rackPosition, tile, squareType, square, row, column)
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
	print(wordsInRowAndScores, 'row&score initial formation')

	# Get scores of words vertically formed
	for word in wordsInColumn:
		for letter in word:
			score += lexicon[letter][0]
		wordsInColumnAndScores.append((word, score))
		score = 0
	print(wordsInColumnAndScores, 'column&score initial formation')

	'''The 3 for loops below correct the score of horizontally formed words'''
	# Corrects score by removing incorrectly added scores from blank tiles
	for move in movesMade:  # Going through stack entries in the move stack
		# Iterate through the index positions and tuples in wordsInRowAndScores
		for i, wordAndScore in enumerate(wordsInRowAndScores):
			# Checks if the letter of the tile placed is in the word AND if the score of the tile placed is 0
			# This is done because score isn't altered, to show that the tile was originally a blank tile
			if move[1].getLetter() in wordAndScore[0] and move[1].getScore() == 0:
				# Updates the wordAndScore by removing the value of the letter being represented by the blank tile
				wordsInRowAndScores[i] = (wordAndScore[0], (wordAndScore[1]-lexicon[move[1].getLetter()][0]))
	print(wordsInRowAndScores, 'row&score after clearing blanks')
	# Corrects score by activating letter multipliers
	for move in movesMade:  # Going through stack entries in the move stack
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
	print(wordsInRowAndScores, 'row&score after letter multipliers')
	# Corrects score by activating word multipliers
	for move in movesMade:  # Going through stack entries in the move stack
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
	print(wordsInRowAndScores, 'row&score after word multipliers')
	'''The 3 for loops below correct the score of vertically formed words'''
	# Corrects score by removing incorrectly added scores from blank tiles
	for move in movesMade:  # Going through stack entries in the move stack
		# Iterate through the index position and tuples in wordsInColumnAndScores
		for i, wordAndScore in enumerate(wordsInColumnAndScores):
			# Checking if the letter of the tile placed is in the word and the score is 0, since this indicates a blank
			if move[1].getLetter() in wordAndScore[0] and move[1].getScore() == 0:
				# Removes the letter's value from the word's score, since a blank tile should award 0 points
				wordsInColumnAndScores[i] = (wordAndScore[0], (wordAndScore[1] - lexicon[move[1].getLetter()][0]))
	print(wordsInColumnAndScores, 'column&score after clearing blanks')
	# Corrects score by activating letter multipliers
	for move in movesMade:  # Going through stack entries in the move stack
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
	print(wordsInColumnAndScores, 'column&score after letter multipliers')
	# Corrects score by activating word multipliers
	for move in movesMade:  # Going through stack entries in the move stack
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
	print(wordsInColumnAndScores, 'column&score after word multipliers')
	# Adding the score of all the words in wordsInRowAndScores
	for wordAndScore in wordsInRowAndScores:
		score += wordAndScore[1]
	# Adding the score of all the words in wordsInColumnAndScores
	for wordAndScore in wordsInColumnAndScores:
		score += wordAndScore[1]

	return score


# Apply post-game penalties
def applyPenalties(player, scoreStolen, lexicon):
	if player.timer.isOvertime:
		# Remove 10 points for every used minute of the overtime timer
		scoreToRemove = -10 * (10 - player.timer.current_seconds // 60)  # Get the decreasing value
		player.score.updateScore(scoreToRemove)  # Updates the score

	if not scoreStolen:
		# Decreases the score of a player by the value of their rack
		scoreToRemove = -1 * player.rack.getTotalScore(lexicon)  # Get the decreasing value
		player.score.updateScore(scoreToRemove)  # Updates the score
	return player


# Read the game file and load in the information
def loadGame(file):

	# Opens the game file and extracts the game dictionary
	with open(os.path.join(os.path.dirname(__file__), f'../data\\{file}.json')) as f:
		gameData = json.load(f)

	language = gameData['Tile Bag']['language']  # Get the language from the tile bag saved

	board = list(gameData['Board'].values())  # Take each row of the saved board & make it a 2D array to form the board
	print(board)
	gameBoard = ScrabbleItemTemplatesV2.Board((400, 10))  # Initialises a game board
	gameBoard = AddSpecialLocations(gameBoard, language)
	gameBoard.replaceBoard(board)  # Replace the empty board with the newly made one
	# TODO: need to update gameBoard.squares somehow, go back and check how it's being updated when a tile is added

	bag = gameData['Tile Bag']['bag']  # Get the bag from the tile bag saved
	TileBag = ScrabbleItemTemplatesV2.TileBag((50, 250), language)  # Initialise a tile bag object
	TileBag.replaceBag(bag)  # Replace the tile bag with the one from the game file
	# TODO: see if below can be altered to achieve the above TODO
	# For loops to go through each square in the board, to create tile objects for the board
	for row in range(15):
		for column in range(15):
			# Checking if the square contains a tile letter
			if gameBoard.getBoard()[row][column] in TileBag.alphabet:
				# Creating a Tile object for that tile
				tile = ScrabbleItemTemplatesV2.Tile(
					f'{language}Letters\\TILE_{gameBoard.getBoard()[row][column]}.png',
					(448+column*48, 58+row*48),
					gameBoard.getBoard()[row][column],
					TileBag.lexicon[gameBoard.getBoard()[row][column]][0])
				tile.transformImage((32, 32))  # Shrinks the tile image so that it fits in the board's square
				tile.canBeClicked = False  # Makes the tile un-clickable
				gameBoard.addToGroup(tile)  # Adds the Tile object to the board group
				gameBoard.squares[row][column] = tile  # Adds the tile to the board's squares array

	TileBag.shuffleCount = 2
	# Must be 2 because a game starts after a tile bag has been shuffled & a game can only be saved after being started.
	P1Name = gameData['Player 1']['Name']
	P1Rack = gameData['Player 1']['Rack']  # Get the contents of Player 1's rack
	P1Score = gameData['Player 1']['Score']  # Get the contents of Player 1's score
	P1TimeLeft = gameData['Player 1']['Timer']['Time Left']  # Get the timer of Player 1
	P1Overtime = gameData['Player 1']['Timer']['Overtime']  # Get the overtime status of Player 1's timer
	Player1 = ScrabbleItemTemplatesV2.Player(P1Name, (550, 775), (1180, 750),
											(1180, 720))
	Player1.rack.replaceContents(P1Rack)  # Update the rack of Player 1
	Player1.rack.fillRackGroup(language, TileBag.lexicon)  # Fill Player 1's rack group
	Player1.score.updateScore(P1Score)  # Update Player 1's score
	Player1.timer.current_seconds = P1TimeLeft  # Update Player 1's timer
	Player1.timer.isOvertime = P1Overtime  # Update the overtime status of Player 1's timer
	if P1Overtime:
		Player1.timer.updateOvertimeTimer()
	else:
		Player1.timer.updateTimer()

	# Must be 2 because a game starts after a tile bag has been shuffled & a game can only be saved after being started.
	P2Name = gameData['Player 2']['Name']
	P2Rack = gameData['Player 2']['Rack']  # Get the contents of Player 2's rack
	P2Score = gameData['Player 2']['Score']  # Get the contents of Player 2's score
	P2TimeLeft = gameData['Player 2']['Timer']['Time Left']  # Get the timer of Player 2
	P2Overtime = gameData['Player 2']['Timer']['Overtime']  # Get the overtime status of Player 2's timer
	Player2 = ScrabbleItemTemplatesV2.Player(P2Name, (550, 775), (1180, 75),
											(1180, 45))
	Player2.rack.replaceContents(P2Rack)  # Update the rack of Player 2
	Player2.rack.fillRackGroup(language, TileBag.lexicon)  # Fill Player 2's rack group
	Player2.score.updateScore(P2Score)  # Update Player 2's score
	Player2.timer.current_seconds = P2TimeLeft  # Update Player 2's timer
	Player2.timer.isOvertime = P2Overtime  # Update the overtime status of Player 2's timer

	if P2Overtime:
		Player2.timer.updateOvertimeTimer()
	else:
		Player2.timer.updateTimer()

	flags = list(gameData['Flags'].values())  # Take the game flags from the game file's dictionary

	return gameBoard, TileBag, Player1, Player2, flags, P1Name, P2Name


# Retrieves the ID of a player
def getPlayerID(username):
	# Opens an SQL connection to the database
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT playerID FROM Players WHERE username=?', (username,))
		userID = cursor.fetchone()
		# Checks if a userID was retrieved
		if userID is not None:
			return userID[0]
		else:
			# If a userID doesn't exist, this means this is a new player. So they need to be added to the Players table.
			cursor.execute('''INSERT INTO Players ('username') VALUES (?)''', (username,))
			cursor.execute('SELECT playerID FROM Players WHERE username=?', (username,))
			return cursor.fetchone()[0]


# Create a record of the current game
def createGameRecord(adminID, Player1_ID, Player2_ID):
	# Opens an SQL connection to the database
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		current_time = datetime.now()  # Gets the exact date and time
		# Create a game record by inserting current_time into the Games table, and then retrieve the game's ID
		cursor.execute('''INSERT INTO Games ('datePlayed') VALUES (?)''', (current_time,))
		cursor.execute('''SELECT gameID FROM Games WHERE datePlayed=?''', (current_time,))
		gameID = cursor.fetchone()[0]
		# Add the game to AdminGames for the administrator moderating the game, and PlayerGames for each player
		cursor.execute('''INSERT INTO AdminGames ('gameID', 'adminID') VALUES (?, ?)''', (gameID, adminID,))
		cursor.execute('''INSERT INTO PlayerGames ('gameID', 'playerID') VALUES (?, ?)''', (gameID, Player1_ID,))
		cursor.execute('''INSERT INTO PlayerGames ('gameID', 'playerID') VALUES (?, ?)''', (gameID, Player2_ID,))
		return gameID


# Fetch the ID of a game using a file name
def getGameID(filename):
	# Open SQL connection to database
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		# Fetching gameID
		cursor.execute('SELECT gameID FROM Games WHERE fileName=?', (filename,))
		return cursor.fetchone()[0]  # Returning gameID


# Add information of a move to the GameHistory table of the database
def addToGameHistory(gameID, moveNumber, playerID, words, score, exchanged, skipped):
	# Opens an SQL connection to the database
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		# Take the details of the move and create a record of the move in the GameHistory table
		cursor.execute('''INSERT INTO GameHistory 
		('gameID', 'moveNumber', 'playerID', 'words', 'score', 'exchanged', 'skipped') 
		VALUES (?, ?, ?, ?, ?, ?, ?)''', (gameID, moveNumber, playerID, words, score, exchanged, skipped,))


# Main subroutine to launch the pygame window and run the game
def createGameWindow(adminID='1', P1Name='', P2Name='', newGameLang=None, gameFile=None):

	pg.init()  # Initialising the pygame window

	SCREEN_WIDTH = pg.display.Info().current_w
	SCREEN_HEIGHT = pg.display.Info().current_h

	win_icon = pg.image.load(os.path.join(os.path.dirname(__file__), '../assets\\images\\EnglishLetters\\TILE_S.png'))
	pg.display.set_icon(win_icon)

	pg.display.set_caption('Scrabble Tournament Game')
	gameWindow = pg.display.set_mode((1600, 900))

	background = pg.Surface((1600, 900))
	background.fill(pg.Color('#3e231e'))

	UIManager = py_gui.UIManager((1600, 900))

	clock = pg.time.Clock()

	fillRack_button = py_gui.elements.UIButton(relative_rect=pg.Rect((84, 650), (100, 50)), text='Fill Rack', manager=UIManager)  # Need to mention ui_button has been edited in the NEA doc
	# fillRack_button.disable()

	shuffleBag_button = py_gui.elements.UIButton(relative_rect=pg.Rect((218, 650), (100, 50)), text='Shuffle', manager=UIManager)  # Commented some code in the UIButton class to prevent pygame.USEREVENT usage
	shuffleBag_button.disable()

	determineOrder_button = py_gui.elements.UIButton(relative_rect=pg.Rect((84, 725), (100, 50)), text='Pick Tile', manager=UIManager)

	swapTurn_button = py_gui.elements.UIButton(relative_rect=pg.Rect((218, 725), (100, 50)), text='Swap', manager=UIManager)
	# swapTurn_button.disable()

	undoMove_button = py_gui.elements.UIButton(relative_rect=pg.Rect((84, 800), (100, 50)), text='Undo Move', manager=UIManager)

	exchangeTile_button = py_gui.elements.UIButton(relative_rect=pg.Rect((218, 800), (100, 50)), text='Exchange', manager=UIManager)

	pg.time.set_timer(pg.USEREVENT, 1000)

	running = True

	flags = [True, False, False, True, False, 2, False, False, False, 0, False, False, False, False, False, False, False, False, False, 1]

	if newGameLang is not None:
		gameBoard, Player1, Player2, TileBag = initialiseScrabbleItems(newGameLang, P1Name, P2Name)
	elif gameFile is not None:
		gameBoard, TileBag, Player1, Player2, flags, P1Name, P2Name = loadGame(gameFile)
	else:
		gameBoard, Player1, Player2, TileBag = initialiseScrabbleItems('English', P1Name, P2Name)

	Player1_ID = getPlayerID(P1Name)
	Player2_ID = getPlayerID(P2Name)

	gameID = None

	if newGameLang is None:
		gameID = getGameID(gameFile)
		print(gameID, 'gameID after loading game')

	print(Player1_ID, 'player1 id')
	print(Player2_ID, 'player2 id')

	Player1_Turn = flags[0]
	orderDetermined = flags[1]
	readyToStart = flags[2]
	firstTurn = flags[3]
	invalidPlay = flags[4]
	blankTilesInPlay = flags[5]
	mustSwapBlank = flags[6]
	blankTileClicked = flags[7]
	exchangeOccurring = flags[8]
	consecutiveZeroPointPlays = flags[9]
	finalScoresAndPenaltiesApplied = flags[10]
	isPaused = flags[11]
	scoreStolen = flags[12]
	gameOver = flags[13]
	revealOtherRack = flags[14]
	spritesAltered = flags[15]
	Player1TileClicked = flags[16]
	Player2TileClicked = flags[17]
	FileNameEntered = flags[18]
	moveNumber = flags[19]

	PauseButton = py_gui.elements.UIButton(relative_rect=pg.Rect((1480, 20), (100, 50)), text='Pause', manager=UIManager)
	PauseButton.disable()

	getLetterToReplace = py_gui.elements.UIWindow(pg.Rect(1210, 338, 400, 300), manager=UIManager, window_display_title='New Letter?')
	getLetterToReplace.hide()

	selectLetterToReplace = py_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=TileBag.alphabet[1:], starting_option='A', relative_rect=pg.Rect((350, 338), (50, 20)), manager=UIManager)
	selectLetterToReplace.hide()

	enterAdminPasswordLabel = ScrabbleItemTemplatesV2.Text((1252, 400), (200, 50), 'Enter Admin Password:')

	enterAdminPassword = py_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pg.Rect((1250, 425), (200, 30)), manager=UIManager)
	enterAdminPassword.disable()
	enterAdminPassword.hide()

	getAdminPassword = py_gui.elements.UIButton(relative_rect=pg.Rect((1460, 425), (75, 30)),  text='Enter', manager=UIManager, text_kwargs={'size': '4'})
	getAdminPassword.hide()
	getAdminPassword.disable()

	cancelClose_button = py_gui.elements.UIButton(relative_rect=pg.Rect((1300, 475), (100, 50)), text='Cancel', manager=UIManager)
	cancelClose_button.hide()
	cancelClose_button.disable()

	# enterPlayer1Name = py_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pg.Rect((1250, 300), (200, 30)), manager=UIManager)
	# enterPlayer1Name.hide()
	# enterPlayer1Name.disable()
	# getPlayer1Name = py_gui.elements.UIButton(relative_rect=pg.Rect((1460, 300), (75, 20)), text='Enter', manager=UIManager, text_kwargs={'size': '4'})
	# getPlayer1Name.hide()
	#
	# P1Name = P1Name
	#
	# enterPlayer2Name = py_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pg.Rect((1250, 400), (200, 30)), manager=UIManager)
	# enterPlayer2Name.hide()
	# enterPlayer2Name.disable()
	# getPlayer2Name = py_gui.elements.UIButton(relative_rect=pg.Rect((1460, 400), (75, 20)), text='Enter', manager=UIManager, text_kwargs={'size': '4'})
	# getPlayer2Name.hide()
	# P2Name = P2Name

	enterFileNameLabel = ScrabbleItemTemplatesV2.Text((1252, 300), (200, 50), 'Enter File Name (min. 6 characters):')

	enterFileName = py_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pg.Rect((1250, 325), (200, 30)), manager=UIManager)
	enterFileName.hide()
	enterFileName.disable()
	getFileName = py_gui.elements.UIButton(relative_rect=pg.Rect((1460, 325), (75, 30)), text='Enter', manager=UIManager, text_kwargs={'size': '4'})
	getFileName.hide()
	getFileName.disable()
	FileName = ''

	invalidPlayWarning = ScrabbleItemTemplatesV2.Text((1210, 338), (200, 100), 'Invalid Play. Try again.')

	movesMade = []  # stack :D
	wordsPlayed = [[], []]

	# intermediateGroup = pg.sprite.Group()

	# damissGroup = pg.sprite.Group()
	# damissterGroup = pg.sprite.Group()

	while running:

		# Set window to 30FPS
		time_delta = clock.tick(30) / 1000.0

		# If players have picked a tile and determined the order, determineOrder_button is killed & shuffleBag_Button is enabled
		if orderDetermined:
			determineOrder_button.kill()
			shuffleBag_button.enable()

		# If the tile bag has been shuffled, the shuffleBag_button is removed, and fillRack_button & swapTurn_button is enabled
		if TileBag.shuffleCount >= 2 and gameID is None:
			shuffleBag_button.kill()
			# fillRack_button.enable()
			# swapTurn_button.enable()


		if mustSwapBlank and not selectLetterToReplace.is_enabled:
			# selectLetterToReplace.show()
			selectLetterToReplace.enable()

		# Going through all events that occur during each tick
		for event in pg.event.get():

			if consecutiveZeroPointPlays == 6 or gameOver:
				revealOtherRack = True

				if Player1_Turn and not spritesAltered:
					Player2.rack.alterSprites()
					# Player2.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon, (1194, 323))
					spritesAltered = True
				elif not Player1_Turn and not spritesAltered:
					Player1.rack.alterSprites()
					# Player1.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon, (1194, 323))
					spritesAltered = True
				if not finalScoresAndPenaltiesApplied:
					Player1 = applyPenalties(Player1, scoreStolen, TileBag.lexicon)
					Player2 = applyPenalties(Player2, scoreStolen, TileBag.lexicon)
					finalScoresAndPenaltiesApplied = True
					if Player1.timer.current_seconds == 0 and Player1.score.isOvertime:
						scoreDiff = Player1.score.getScore() - Player2.score.getScore()
						if scoreDiff > -1:
							Player2.score.updateScore(scoreDiff+1)
					if Player2.timer.current_seconds == 0 and Player2.score.isOvertime:
						scoreDiff = Player2.score.getScore() - Player1.score.getScore()
						if scoreDiff > -1:
							Player2.score.updateScore(scoreDiff+1)
				if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
					# hide text
					enterAdminPassword.set_text_hidden()
				# if cancelClose_button.is_enabled == 0:
				# 	cancelClose_button.show()
				# 	cancelClose_button.enable()
				# if enterPlayer1Name.is_enabled == 0:
				# 	getPlayer1Name.show()
				# 	getPlayer1Name.enable()
				# 	enterPlayer1Name.show()
				# 	enterPlayer1Name.enable()
				# if enterPlayer2Name.is_enabled == 0:
				# 	getPlayer2Name.show()
				# 	getPlayer2Name.enable()
				# 	enterPlayer2Name.show()
				# 	enterPlayer2Name.enable()
				if enterFileName.is_enabled == 0:
					enterFileName.show()
					enterFileName.enable()
					getFileName.show()
					getFileName.enable()
				if getAdminPassword.is_enabled == 0:
					getAdminPassword.show()
					getAdminPassword.enable()
					enterAdminPassword.show()
					enterAdminPassword.enable()
					enterAdminPassword.set_text_hidden()
				if swapTurn_button.is_enabled == 1:
					# disable
					swapTurn_button.disable()
				if exchangeTile_button.is_enabled == 1:
					# disable
					exchangeTile_button.disable()
				if undoMove_button.is_enabled == 1:
					undoMove_button.disable()
				if PauseButton.is_enabled == 1:
					PauseButton.disable()

				if event.type == py_gui.UI_BUTTON_PRESSED:
					if event.ui_element == enterAdminPassword:
						print('button has been pressed')
						correctPasswordEntered = verifyAdminPassword(enterAdminPassword.get_text(), adminID)
						if correctPasswordEntered:
							running = False
							break

					# if event.ui_element == enterPlayer1Name:
					# 	P1Name = enterPlayer1Name.get_text()
					# 	P1NameEntered = True
					#
					# if event.ui_element == enterPlayer2Name:
					# 	P2Name = enterPlayer2Name.get_text()
					# 	P2NameEntered = True

					if event.ui_element == enterFileName:
						FileName = enterFileName.get_text()
						FileNameEntered = True

			if event.type == pg.QUIT and readyToStart:
				invalidPlay = False
				if PauseButton.is_enabled == 1:
					# disable
					PauseButton.disable()
				if swapTurn_button.is_enabled == 1:
					# disable
					swapTurn_button.disable()
				if exchangeTile_button.is_enabled:
					# disable
					exchangeTile_button.disable()
				if undoMove_button.is_enabled == 1:
					# disable
					undoMove_button.disable()
				if not isPaused and not gameOver:
					# pause game
					isPaused = True
				if cancelClose_button.is_enabled == 0:
					cancelClose_button.show()
					cancelClose_button.enable()
				# if enterPlayer1Name.is_enabled == 0:
				# 	getPlayer1Name.show()
				# 	getPlayer1Name.enable()
				# 	enterPlayer1Name.show()
				# 	enterPlayer1Name.enable()
				# if enterPlayer2Name.is_enabled == 0:
				# 	getPlayer2Name.show()
				# 	getPlayer2Name.enable()
				# 	enterPlayer2Name.show()
				# 	enterPlayer2Name.enable()
				if enterFileName.is_enabled == 0:
					enterFileName.show()
					enterFileName.enable()
					getFileName.show()
					getFileName.enable()
				if enterAdminPassword.is_enabled == 0:
					enterAdminPassword.show()
					enterAdminPassword.enable()
					getAdminPassword.show()
					getAdminPassword.enable()
					enterAdminPassword.set_text_hidden()
			elif event.type == pg.QUIT and not readyToStart:
				running = False
				break

			# if user closes the window
			# if event.type == pg.QUIT and not gameOver:
			#     if getAdminPassword.is_enabled == 0:
			#         getAdminPassword.show()
			#         getAdminPassword.enable()
			#         getAdminPassword.set_text_hidden()
			#         enterAdminPassword.show()
			#         enterAdminPassword.enable()
			#         cancelClose_button.show()
			#         cancelClose_button.enable()
			#     running = False
			#     break

			# if a pygame_gui button has been pressed
			if event.type == py_gui.UI_BUTTON_PRESSED:

				if event.ui_element == getAdminPassword and FileNameEntered:
					print('button has been pressed')
					correctPasswordEntered = verifyAdminPassword(enterAdminPassword.get_text(), adminID)
					if correctPasswordEntered:
						running = False
						break

				# if event.ui_element == getPlayer1Name:
				# 	P1Name = enterPlayer1Name.get_text()
				# 	P1NameEntered = True
				# 	print(P1Name, P1NameEntered)
				#
				# if event.ui_element == getPlayer2Name:
				# 	P2Name = enterPlayer2Name.get_text()
				# 	P2NameEntered = True
				# 	print(P2Name, P2NameEntered)

				if event.ui_element == getFileName:
					FileName = enterFileName.get_text()
					if len(FileName) > 5 and FileName.isalnum():
						FileNameEntered = True
					else:
						if len(FileName) <= 5:
							CTkMessagebox(title='Error!', message='Filename must be at least 6 characters long.', width=160, height=80, sound=True)
						if not FileName.isalnum():
							CTkMessagebox(title='Error!', message='Invalid filename.', width=160, height=80, sound=True)
					print(FileName, FileNameEntered)

				if event.ui_element == cancelClose_button:
					# getPlayer1Name.hide()
					# getPlayer1Name.disable()
					# enterPlayer1Name.hide()
					# enterPlayer1Name.disable()
					# getPlayer2Name.hide()
					# getPlayer2Name.disable()
					# enterPlayer2Name.hide()
					# enterPlayer2Name.disable()
					getFileName.hide()
					getFileName.disable()
					enterFileName.hide()
					enterFileName.disable()
					getAdminPassword.hide()
					getAdminPassword.disable()
					enterAdminPassword.hide()
					enterAdminPassword.disable()
					cancelClose_button.hide()
					cancelClose_button.disable()
					PauseButton.enable()
					swapTurn_button.enable()
					exchangeTile_button.enable()
					undoMove_button.enable()
					isPaused = False

				if event.ui_element == PauseButton and not gameOver:
					if not isPaused:
						PauseButton.text = 'Resume'
						PauseButton.rebuild()
						exchangeTile_button.disable()
						swapTurn_button.disable()
						undoMove_button.disable()
						isPaused = True
					else:
						PauseButton.text = 'Pause'
						PauseButton.rebuild()
						exchangeTile_button.enable()
						swapTurn_button.enable()
						undoMove_button.enable()
						isPaused = False

				if event.ui_element == exchangeTile_button and (Player1TileClicked or Player2TileClicked) and not (gameOver or isPaused):
					blankTileClicked = False
					mustSwapBlank = False
					selectLetterToReplace.hide()
					print('exchange button clicked')
					if Player1TileClicked:
						print('player 1 initiating exchange')
						Player1, TileBag, Player1TileClicked = findTileToExchange(Player1, TileBag)
					else:
						Player2, TileBag, Player2TileClicked = findTileToExchange(Player2, TileBag)
					exchangeOccurring = True

				# if fillRack_button has been pressed
				if event.ui_element == fillRack_button and TileBag.shuffleCount >= 2 and not gameOver:
					Player1.rack.fillRack(TileBag)
					Player1.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)
					Player2.rack.fillRack(TileBag)
					Player2.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)
					readyToStart = True
					fillRack_button.disable()
					PauseButton.enable()
					if newGameLang is not None:
						gameID = createGameRecord(adminID, Player1_ID, Player2_ID)

				# if shuffleBag_button has been pressed
				if event.ui_element == shuffleBag_button:
					# Shuffle bag
					TileBag.shuffleBag()

				if event.ui_element == undoMove_button and not (gameOver or isPaused):
					# undo move
					gameBoard, stack, Player1, Player2 = undoPlay(gameBoard, movesMade, Player1_Turn, Player1, Player2, TileBag.getLanguage())
					blankTileClicked = False
					selectLetterToReplace.hide()

				# if swapTurn_button has been pressed
				if event.ui_element == swapTurn_button and TileBag.shuffleCount >= 2 and not (gameOver or isPaused):
					if not exchangeOccurring:  # check board now
						valid, wordsCreated = checkTurn(gameBoard, movesMade, TileBag.getLanguage(), TileBag.alphabet, firstTurn, wordsPlayed)
						print(valid, wordsCreated, 'valid n wordsmade after checkTurn()')
						print(wordsCreated, 'wordsCreated')
						if valid:
							if not (len(wordsCreated[0]) == 0 and len(wordsCreated[1]) == 0):
								valid = checkWords(wordsCreated, TileBag.getLanguage())
								if valid:  # need to code in awarding the score
									print('valid turn')
									score = calculateScore(wordsCreated, movesMade, TileBag.lexicon)
									print(score, 'score calc\'ed')
									Player1_Turn = not Player1_Turn
									firstTurn = False
									if Player1_Turn:
										if not TileBag.isEmpty():
											if len(movesMade) == 7:
												score += 50
											print(score, 'score for player2')
											Player2.rack.fillRack(TileBag)
											Player2.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)
											Player2.score.updateScore(score)
										else:
											if Player2.rack.isEmpty():
												scoreToSteal = Player1.rack.getTotalScore(TileBag.lexicon)
												Player2.score.updateScore(scoreToSteal*2)
												gameOver = True
												scoreStolen = True
									else:
										if not TileBag.isEmpty():
											if len(movesMade) == 7:
												score += 50
											print(score, 'score for player1')
											Player1.rack.fillRack(TileBag)
											Player1.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)
											Player1.score.updateScore(score)
										else:
											if Player1.rack.isEmpty():
												scoreToSteal = Player2.rack.getTotalScore(TileBag.lexicon)
												Player1.score.updateScore(scoreToSteal*2)
												gameOver = True
												scoreStolen = True
									invalidPlay = False
									print(movesMade)
									wordsCreatedString = ','.join(wordsCreated[0])+','+','.join(wordsCreated[1])
									if Player1_Turn:
										addToGameHistory(gameID, moveNumber, Player2_ID, wordsCreatedString, score, exchangeOccurring, bool(len(wordsCreated[0]) == 0 and len(wordsCreated[1]) == 0))
									else:
										addToGameHistory(gameID, moveNumber, Player1_ID, wordsCreatedString, score, exchangeOccurring, bool(len(wordsCreated[0]) == 0 and len(wordsCreated[1]) == 0))
									if blankTilesInPlay == 0:
										selectLetterToReplace.kill()
									else:
										selectLetterToReplace.disable()
										selectLetterToReplace.hide()
									moveNumber += 1
									movesMade = []
									for i, row in enumerate(wordsCreated):
										for word in row:
											wordsPlayed[i].append(word)
									# old code below

									# for word in wordsCreated:
									#     wordsPlayed.append(word)
									consecutiveZeroPointPlays = 0

								else:
									gameBoard, stack, Player1, Player2 = undoPlay(gameBoard, movesMade, Player1_Turn, Player1, Player2, TileBag.getLanguage())
									invalidPlay = True
									print('invalid turn')
							else:
								Player1_Turn = not Player1_Turn
								if Player1_Turn:
									addToGameHistory(gameID, moveNumber, Player2_ID, '', 0, exchangeOccurring, bool(len(wordsCreated[0]) == 0 and len(wordsCreated[1]) == 0))
								else:
									addToGameHistory(gameID, moveNumber, Player1_ID, '', 0, exchangeOccurring, bool(len(wordsCreated[0]) == 0 and len(wordsCreated[1]) == 0))
								consecutiveZeroPointPlays += 1
								moveNumber += 1
						else:
							gameBoard, stack, Player1, Player2 = undoPlay(gameBoard, movesMade, Player1_Turn, Player1, Player2, TileBag.getLanguage())
							invalidPlay = True
							print('invalid turn')
					else:
						Player1_Turn = not Player1_Turn
						if Player1_Turn:
							sprites = Player2.rack.getSprites()
							for i in range(7):
								sprites[f'TILE{i+1}'].canBeClicked = True
								sprites[f'TILE{i+1}'].updateImage(f"{TileBag.getLanguage()}Letters\\TILE_{Player2.rack.getContents()[i]}.png")
							Player2.rack.updateSprites(sprites)
							addToGameHistory(gameID, moveNumber, Player2_ID, '', 0, exchangeOccurring, False)
						else:
							sprites = Player1.rack.getSprites()
							for i in range(7):
								sprites[f'TILE{i + 1}'].canBeClicked = True
								sprites[f'TILE{i + 1}'].updateImage(f"{TileBag.getLanguage()}Letters\\TILE_{Player1.rack.getContents()[i]}.png")
							Player1.rack.updateSprites(sprites)
							addToGameHistory(gameID, moveNumber, Player1_ID, '', 0, exchangeOccurring, False)
						consecutiveZeroPointPlays += 1
						moveNumber += 1
						exchangeOccurring = False

				# If determineOrder_button has been pressed
				if event.ui_element == determineOrder_button and not gameOver:
					Player1Tile = ''
					Player2Tile = ''

					while Player1Tile == Player2Tile:
						Player1Tile = pickTile(TileBag)
						Player2Tile = pickTile(TileBag)

					if TileBag.alphabet.index(Player1Tile) > TileBag.alphabet.index(Player2Tile):
						Player1, Player2 = swapPlayers(Player1, Player2)
						print('swapped players')
					else:
						print('nuh uh on dat swapparooney)')
					orderDetermined = True

			# Used to decrement the timer
			if event.type == pg.USEREVENT and readyToStart and not (gameOver or isPaused):
				if Player1.timer.current_seconds != 0 and Player1_Turn and not gameOver:
					Player1.timer.current_seconds -= 1
					if not Player1.timer.isOvertime:
						Player1.timer.updateTimer()
					else:
						Player1.timer.updateOvertimeTimer()
					if consecutiveZeroPointPlays == 6:
						gameOver = True
					if Player1.timer.current_seconds == 0 and not Player1.timer.isOvertime and not gameOver:
						Player1.replaceTimer()
					elif Player1.timer.current_seconds == 0 and Player1.timer.isOvertime:
						gameOver = True

				if Player2.timer.current_seconds != 0 and not Player1_Turn and not gameOver:
					Player2.timer.current_seconds -= 1
					if not Player2.timer.isOvertime:
						Player2.timer.updateTimer()
					else:
						Player2.timer.updateOvertimeTimer()
					if consecutiveZeroPointPlays == 6:
						gameOver = True
					if Player2.timer.current_seconds == 0 and not Player2.timer.isOvertime and not gameOver:
						Player2.replaceTimer()
					elif Player2.timer.current_seconds == 0 and Player2.timer.isOvertime:
						gameOver = True
			# if event.type == pg.USEREVENT and blankTileClicked:
			if event.type == py_gui.UI_DROP_DOWN_MENU_CHANGED and not isPaused:
				if event.ui_element == selectLetterToReplace:
					movesMade, blankTileClicked, gameBoard = swapBlankToLetter(movesMade, event.text, TileBag.getLanguage(), gameBoard)
					blankTilesInPlay -= 1
					blankTileClicked = False
					mustSwapBlank = False

			if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0] and not (gameOver or isPaused):
				mouse_pos = pg.mouse.get_pos()

				if Player1_Turn and not Player1TileClicked and (584 <= mouse_pos[0] <= 1016) and (798 <= mouse_pos[1] <= 846) and not blankTileClicked:
					print('a tile has been clicked on by player1')
					Player1TileClicked, blankTileClicked = selectTile(Player1, mouse_pos)
					print(Player1TileClicked, 'player1tileclicked', blankTileClicked, 'blanktileclicked - PLAYER1')
					if blankTileClicked and not exchangeOccurring:
						selectLetterToReplace.show()
						selectLetterToReplace.disable()
				elif Player1_Turn and Player1TileClicked and (448 <= mouse_pos[0] <= 1152) and (58 <= mouse_pos[1] <= 762) and not exchangeOccurring:
					row, column = selectSquare(gameBoard, mouse_pos)
					print(row, column, 'square selected - PLAYER1')
					if not (row == -1 and column == -1):
						Player1TileClicked, tileToMove, movesMade = getTileToMove(Player1, movesMade)
						gameBoard, specialLocation, movesMade = moveTile(gameBoard, row, column, tileToMove, movesMade)
						if blankTileClicked:
							mustSwapBlank = True
				elif not Player1_Turn and not Player2TileClicked and (584 <= mouse_pos[0] <= 1016) and (798 <= mouse_pos[1] <= 846) and not blankTileClicked:
					print('a tile has been clicked on by player2')
					Player2TileClicked, blankTileClicked = selectTile(Player2, mouse_pos)
					print(Player2TileClicked, 'player1tileclicked', blankTileClicked, 'blanktileclicked - PLAYER2')
					if blankTileClicked and not exchangeOccurring:
						selectLetterToReplace.show()
						selectLetterToReplace.disable()
				elif not Player1_Turn and Player2TileClicked and (448 <= mouse_pos[0] <= 1152) and (58 <= mouse_pos[1] <= 762) and not exchangeOccurring:
					row, column = selectSquare(gameBoard, mouse_pos)
					print(row, column, 'square selected - PLAYER2')
					if not (row == -1 and column == -1):
						Player2TileClicked, tileToMove, movesMade = getTileToMove(Player2, movesMade)
						gameBoard, specialLocation, movesMade = moveTile(gameBoard, row, column, tileToMove, movesMade)
						if blankTileClicked:
							mustSwapBlank = True

			# Processing anything pygame_gui related for the event
			UIManager.process_events(event)

		# Update game window, draw background, and draw buttons
		UIManager.update(time_delta)
		gameWindow.blit(background, (0, 0))
		UIManager.draw_ui(gameWindow)

		# Blit the board and tile bag
		gameWindow.blit(gameBoard.getImage(), (gameBoard.getRectCoordinates()))
		gameWindow.blit(TileBag.getImage(), (TileBag.getRectCoordinates()))

		# Blit the rack and tiles for whose turn it is
		if Player1_Turn and not gameOver:
			gameWindow.blit(Player1.rack.getImage(), (Player1.rack.getRectCoordinates()))
			gameWindow.blit(ScrabbleItemTemplatesV2.Text((568, 875), (200, 100), f'{Player1.name} - Player 1').text, (568, 875))
			# Player1.rack.drawGroup(gameWindow)
			Player1.rack.getGroup().draw(gameWindow)
		elif not Player1_Turn and not gameOver:

			gameWindow.blit(Player2.rack.getImage(), (Player2.rack.getRectCoordinates()))
			gameWindow.blit(ScrabbleItemTemplatesV2.Text((568, 875), (200, 100), f'{Player2.name} - Player 2').text, (568, 875))
			# Player2.rack.drawGroup(gameWindow)
			Player2.rack.getGroup().draw(gameWindow)

		# Blit the score and timer for both players
		gameWindow.blit(Player1.timer.text, Player1.timer.getRectCoordinates())
		gameWindow.blit(Player1.score.text, Player1.score.getRectCoordinates())

		gameWindow.blit(Player2.timer.text, Player2.timer.getRectCoordinates())
		gameWindow.blit(Player2.score.text, Player2.score.getRectCoordinates())

		if revealOtherRack and Player1_Turn:
			gameWindow.blit(Player2.rack.getImage(), (1050, 775))
			gameWindow.blit(ScrabbleItemTemplatesV2.Text((1068, 875), (200, 100), f'{Player2.name} - Player 2').text, (1068, 875))
			gameWindow.blit(ScrabbleItemTemplatesV2.Text((568, 875), (200, 100), f'{Player1.name} - Player 1').text, (568, 875))
			Player2.rack.getGroup().draw(gameWindow)
			gameWindow.blit(Player1.rack.getImage(), Player1.rack.getRectCoordinates())
			Player1.rack.getGroup().draw(gameWindow)
		elif revealOtherRack and not Player1_Turn:
			gameWindow.blit(Player1.rack.getImage(), (1050, 775))
			gameWindow.blit(ScrabbleItemTemplatesV2.Text((1068, 875), (200, 100), f'{Player1.name} - Player 1').text, (1068, 875))
			gameWindow.blit(ScrabbleItemTemplatesV2.Text((568, 875), (200, 100), f'{Player2.name} - Player 2').text, (568, 875))
			Player1.rack.getGroup().draw(gameWindow)
			gameWindow.blit(Player2.rack.getImage(), Player2.rack.getRectCoordinates())
			Player2.rack.getGroup().draw(gameWindow)

		if getFileName.is_enabled == 1:
			gameWindow.blit(enterFileNameLabel.text, enterFileNameLabel.rect)
		if getAdminPassword.is_enabled == 1:
			gameWindow.blit(enterAdminPasswordLabel.text, enterAdminPasswordLabel.rect)

		if invalidPlay:
			gameWindow.blit(invalidPlayWarning.text, (invalidPlayWarning.rect.x, invalidPlayWarning.rect.y))

		for row in gameBoard.squares:
			for square in row:
				if isinstance(square, ScrabbleItemTemplatesV2.Square):
					x, y = square.getRectCoordinates()
					gameWindow.blit(square.getText(), (x+2, y+6))

		gameBoard.getGroup().draw(gameWindow)
		# damissterGroup.draw(gameWindow)

		pg.display.update()

	pg.quit()

	boardDict = {
		'1': gameBoard.getBoard()[0],
		'2': gameBoard.getBoard()[1],
		'3': gameBoard.getBoard()[2],
		'4': gameBoard.getBoard()[3],
		'5': gameBoard.getBoard()[4],
		'6': gameBoard.getBoard()[5],
		'7': gameBoard.getBoard()[6],
		'8': gameBoard.getBoard()[7],
		'9': gameBoard.getBoard()[8],
		'10': gameBoard.getBoard()[9],
		'11': gameBoard.getBoard()[10],
		'12': gameBoard.getBoard()[11],
		'13': gameBoard.getBoard()[12],
		'14': gameBoard.getBoard()[13],
		'15': gameBoard.getBoard()[14]
	}

	tileBagDict = {
		'bag': TileBag.bag,
		'language': TileBag.getLanguage()
	}

	Player1Dict = {
		'Name': Player1.name,
		'Rack': Player1.rack.getContents(),
		'Score': Player1.score.getScore(),
		'Timer': {
			'Time Left': Player1.timer.current_seconds,
			'Overtime': Player1.timer.isOvertime
		}

	}

	Player2Dict = {
		'Name': Player2.name,
		'Rack': Player2.rack.getContents(),
		'Score': Player2.score.getScore(),
		'Timer': {
			'Time Left': Player2.timer.current_seconds,
			'Overtime': Player2.timer.isOvertime
		}
	}

	flagsDict = {
		"Player1_Turn": Player1_Turn,
		"orderDetermined": orderDetermined,
		"readyToStart": readyToStart,
		"firstTurn": firstTurn,
		"invalidPlay": invalidPlay,
		"blankTilesInPlay": blankTilesInPlay,
		"mustSwapBlank": mustSwapBlank,
		"blankTileClicked": blankTileClicked,
		"exchangeOccurring": exchangeOccurring,
		"consecutiveZeroPointPlays": consecutiveZeroPointPlays,
		"finalScoresAndPenaltiesApplied": finalScoresAndPenaltiesApplied,
		"isPaused": isPaused,
		"scoreStolen": scoreStolen,
		"gameOver": gameOver,
		"revealOtherRack": revealOtherRack,
		"spritesAltered": spritesAltered,
		"Player1TileClicked": Player1TileClicked,
		"Player2TileClicked": Player2TileClicked,
		"FileNameEntered": FileNameEntered,
		"moveNumber": moveNumber
	}

	gameDict = {
		'Board': boardDict,
		'Tile Bag': tileBagDict,
		'Player 1': Player1Dict,
		'Player 2': Player2Dict,
		'Flags': flagsDict
	}

	if gameOver:
		if Player1Dict['Score'] > Player2Dict['Score']:
			# bleh
			winner = f"Winner: {Player1Dict['Name']}"
		elif Player2Dict['Score'] > Player1Dict['Score']:
			# blah
			winner = f"Winner: {Player2Dict['Name']}"
		else:
			# update to reflect it's a tie
			winner = 'Tie'
	else:
		winner = ''

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

	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		cursor.execute('''UPDATE Games SET fileName=?, result=? WHERE gameID=?''', (FileName, winner, gameID,))

	CTkMessagebox(title='Success!', message='Game saved successfully. Goodbye!')
