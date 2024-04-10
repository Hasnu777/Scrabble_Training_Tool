import pygame as pg
import json
import pygame_gui as py_gui
import random
import sqlite3 as sql
import os
from gameLogic import ScrabbleItemTemplatesV2
from datetime import datetime


def initialiseScrabbleItems(language, P1Name, P2Name):

	gameBoard = ScrabbleItemTemplatesV2.Board((400, 10))
	gameBoard = AddSpecialLocations(gameBoard)

	Player1 = ScrabbleItemTemplatesV2.Player(P1Name, (550, 775), (1180, 750), (1180, 720))

	Player2 = ScrabbleItemTemplatesV2.Player(P2Name, (550, 775), (1180, 75), (1180, 45))

	TileBag = ScrabbleItemTemplatesV2.TileBag((50, 250), language)

	return gameBoard, Player1, Player2, TileBag


def AddSpecialLocations(board):
	for bonusType in ScrabbleItemTemplatesV2.SpecialLocations.keys():
		for position in ScrabbleItemTemplatesV2.SpecialLocations[bonusType]:
			board.addToBoard(position[0], position[1], bonusType)
			board.squares[position[0]][position[1]] = ScrabbleItemTemplatesV2.Square(
				((448+position[1]*48), (58+position[0]*48)), text=bonusType)
	return board


def selectSquare(board, mouse_pos):
	row = -1
	column = -1
	for i in range(15):
		for j in range(15):
			try:
				square: ScrabbleItemTemplatesV2.Square = board.squares[i][j]
				if square.getSquareRect().collidepoint(mouse_pos):
					row = i
					column = j
			except AttributeError:
				continue
	return row, column


def pickTile(tileBag):
	item = random.choice(tileBag.bag[:-1])
	indexPosition = tileBag.bag.index(item)
	letter = tileBag.bag[indexPosition][0]
	return letter


def swapPlayers(player1, player2):
	player1.rack, player2.rack = player2.rack, player1.rack
	player1.timer, player2.timer = player2.timer, player1.timer
	player1.score, player2.score = player2.score, player1.score
	return player2, player1


def selectTile(player, mouse_pos):
	for i, tile in enumerate(player.rack.getSprites().values()):
		print(i, 'count')
		if tile is not None and tile.getRect().collidepoint(mouse_pos):
			print(tile.getLetter(), i, 'tile letter')
			print(tile.canBeClicked, 'tile can be clicked')
			if tile.canBeClicked:
				tile.isClicked = True
				if tile.getLetter() == '!':
					return True, True
				else:
					return True, False
			else:
				return False, False
	return False, False


def getTileToMove(player, stack):
	for i, tile in enumerate(player.rack.getSprites().values()):
		if tile is not None:
			if tile.isClicked:
				tile.isClicked = False
				player.rack.removeFromRack(i, tile)
				stack.append((i, tile))
				return False, tile, stack


def moveTile(board, row, column, tile, stack):
	specialLocation = board.CheckForSpecialLocation(row, column)  # previous tile (' ' or TW/DW/TL/DL)
	board.addToBoard(row, column, tile.getLetter())  # puts tile letter in board
	square = board.squares[row][column]  # takes square from board
	tile.updateRect(square.getRectCoordinates())  # moves tile sprite to square location
	tile.transformImage((32, 32))  # resizes tile image to 32x32
	tile.isClicked = False
	board.squares[row][column] = tile  # puts tile sprite into squares
	board.addToGroup(tile)  # adds tile to board Group
	stack[-1] = (stack[-1][0], stack[-1][1], specialLocation, square, row, column)
	return board, specialLocation, stack


def checkTurn(gameBoard, stack, language, alphabet, firstTurn, wordsPlayed):
	validPlay = False

	board = gameBoard.getBoard()
	wordsOnBoard = [[], []]
	wordsInRow = ''
	for row in board:
		for letter in row:
			if letter in alphabet:
				wordsInRow += letter
			else:
				if language == 'English':
					if len(wordsInRow) > 1 and wordsInRow not in ('RR', 'LL'):
						wordsOnBoard[0].append(wordsInRow)
				else:
					if len(wordsInRow) > 1 and wordsInRow not in ('CH', 'RR', 'LL'):
						wordsOnBoard[0].append(wordsInRow)
				wordsInRow = ''
	if language == 'English':
		if len(wordsInRow) > 1 and wordsInRow not in ('RR', 'LL'):
			wordsOnBoard[0].append(wordsInRow)
	else:
		if len(wordsInRow) > 1 and wordsInRow not in ('CH', 'RR', 'LL'):
			wordsOnBoard[0].append(wordsInRow)
	wordsInColumn = ''

	for column in range(15):
		for row in range(15):
			if board[row][column] in alphabet:
				wordsInColumn += board[row][column]
			else:
				if language == 'English':
					if len(wordsInColumn) > 1 and wordsInColumn not in ('RR', 'LL'):
						wordsOnBoard[1].append(wordsInColumn)
				else:
					if len(wordsInColumn) > 1 and wordsInColumn not in ('CH', 'RR', 'LL'):
						wordsOnBoard[1].append(wordsInColumn)
				wordsInColumn = ''
		if language == 'English':
			if len(wordsInColumn) > 1 and wordsInColumn not in ('RR', 'LL'):
				wordsOnBoard[1].append(wordsInColumn)
		else:
			if len(wordsInColumn) > 1 and wordsInColumn not in ('CH', 'RR', 'LL'):
				wordsOnBoard[1].append(wordsInColumn)
		wordsInColumn = ''

	wordsCreated = [[], []]

	for word in wordsOnBoard[0]:
		if wordsOnBoard[0].count(word) > wordsPlayed[0].count(word):
			for i in range(wordsOnBoard[0].count(word)-wordsPlayed[0].count(word)):
				wordsCreated[0].append(word)

	for word in wordsOnBoard[1]:
		if wordsOnBoard[1].count(word) > wordsPlayed[1].count(word):
			for i in range(wordsOnBoard[1].count(word)-wordsPlayed[1].count(word)):
				wordsCreated[1].append(word)

	# old code below

	# print(wordsOnBoard, 'wordsOnBoard')
	# print(wordsPlayed, 'wordsPlayed')
	# for word in wordsOnBoard:
	#     if wordsOnBoard.count(word) > wordsPlayed.count(word):
	#         for i in range(wordsOnBoard.count(word)-wordsPlayed.count(word)):
	#             wordsCreated.append(word)
	print(wordsCreated, 'wordsCreated')

	if firstTurn:
		if not (len(wordsCreated[0]) == 0 and len(wordsCreated[1]) == 0):
			print('tis the first turn')
			for move in stack:
				print(move[1].getRectCoordinates(), 'rect coords')
				validPlay = (move[1].getRectCoordinates() == (784, 394))
				print(validPlay, 'for tile on center square')
				if validPlay:
					print('tile detected on center square')
					break
			if not validPlay:
				print('no tile detected on center square')
				print(validPlay, 'for valid play now')
				return validPlay, []
		else:
			validPlay = True
	else:
		validPlay = True

	return validPlay, wordsCreated


def undoPlay(board, stack, PlayerTurn, Player1, Player2, language):
	if not stack:
		return board, stack, Player1, Player2
	else:
		rackPosition, tile, squareType, square, row, column = stack.pop()  # (rackPosition, tile, squareType, square, row, column)
		board.removeFromGroup(tile)
		board.squares[row][column] = square
		tile.updateRect((584+rackPosition*64, 798))
		if tile.getScore() == 0:
			tile.updateLetter('!')
			tile.updateImage(f'FrenchLetters\\TILE_!.png')
		else:
			tile.updateImage(f'{language}Letters\\TILE_{tile.getLetter()}.png')
		board.getBoard()[row][column] = squareType
		if PlayerTurn:
			Player1.rack.addToRack(rackPosition, tile)
		else:
			Player2.rack.addToRack(rackPosition, tile)
		return undoPlay(board, stack, PlayerTurn, Player1, Player2, language)


def undoMove(board, stack, PlayerTurn, Player1, Player2):
	if not stack:
		return board, stack, Player1, Player2
	rackPosition, tile, squareType, square, row, column = stack.pop()  # (rackPosition, tile, squareType, square, row, column)
	board.removeFromGroup(tile)
	board.squares[row][column] = square
	tile.updateRect((584 + rackPosition * 64, 798))
	tile.transformImage((48, 48))
	board.getBoard()[row][column] = squareType
	if PlayerTurn:
		Player1.rack.addToRack(rackPosition, tile)
	else:
		Player2.rack.addToRack(rackPosition, tile)
	return board, stack, Player1, Player2


def checkWords(wordsToCheck, language):
	conn = sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db'))
	cursor = conn.cursor()
	for row in wordsToCheck:  # new for loop to handle wordsToCheck being a 2D array
		for word in row:
			print(word)
			cursor.execute(f'SELECT words FROM {language}Words WHERE words=?', (word,))
			wordFetched = cursor.fetchone()
			print(wordFetched)
			if wordFetched is None:
				return False
			if word != wordFetched[0]:
				return False
	return True


def swapBlankToLetter(stack, letter, language, gameboard):
	moveMade = stack[-1]
	tile = moveMade[1]
	gameboard.removeFromGroup(tile)
	tile.updateLetter(letter)
	tile.updateImage(f'{language}Letters\\TILE_{letter}_BLANK.png')
	tile.transformImage((32, 32))
	gameboard.getBoard()[moveMade[-2]][moveMade[-1]] = tile.getLetter()
	gameboard.addToGroup(tile)
	moveMade = (moveMade[0], tile, moveMade[2], moveMade[3], moveMade[4], moveMade[5])
	stack[-1] = moveMade
	return stack, False, gameboard


def findTileToExchange(player, tileBag):
	for i, tile in enumerate(player.rack.getSprites().values()):
		print(i, 'find exchange tile count')
		if tile is not None:
			print(tile.getLetter(), i, 'tile being exchanged')
			print(tile.isClicked, 'tile can be clicked')
			if tile.isClicked:
				tileToExchange = tile
				tileToExchangePosition = i
				return exchangeTile(player, tileToExchange, tileToExchangePosition, tileBag)


def exchangeTile(player, tileToExchange, tileToExchangePosition, tileBag):
	player.rack.removeFromRack(tileToExchangePosition, tileToExchange)
	print(player.rack.getContents())
	letterToExchange = tileToExchange.getLetter()
	newTileInfo = None
	newTileInfoPosition = -1
	print(tileBag.bag)
	for i, tile in enumerate(tileBag.bag):
		print(i, 'count for finding letter to put exchanging tile back inside tilebag')
		print(tile[0])
		if letterToExchange == tile[0]:
			newTileInfo = (tile[0], tile[1], (tile[2]+1))
			newTileInfoPosition = i
			print(newTileInfo, newTileInfoPosition, 'new letter info and its position in tile bag')
			break
	if newTileInfo[2] == 1:
		tileBag.bag[-1] += 1
	print(tileBag.bag[newTileInfoPosition])
	tileBag.bag[newTileInfoPosition] = newTileInfo
	player.rack.fillRack(tileBag)
	player.rack.fillRackGroup(tileBag.getLanguage(), tileBag.lexicon, (584, 798))
	spritesList = player.rack.getSprites()
	newTile = spritesList[f'TILE{tileToExchangePosition+1}']
	print(newTile.getLetter(), 'newTile that was put into rack')
	newTile.canBeClicked = False
	newTile.updateImage('TILE_UNKNOWN.png')
	spritesList[f'TILE{tileToExchangePosition+1}'] = newTile
	player.rack.updateSprites(spritesList)
	return player, tileBag, False


def verifyAdminPassword(password, IDToUse):
	conn = sql.connect(os.path.join(os.path.dirname(__file__), '../scrabbleTrainingTool.db'))
	cursor = conn.cursor()
	cursor.execute('SELECT password FROM users WHERE id=?', (IDToUse,))
	daPassword = cursor.fetchone()
	print(daPassword)
	if password == daPassword[0]:
		return True


def calculateScore(wordsCreated, movesMade, lexicon):  # (rackPosition, tile, squareType, square, row, column)
	wordsInRow = wordsCreated[0]
	wordsInColumn = wordsCreated[1]
	wordsInRowAndScores = []
	wordsInColumnAndScores = []
	score = 0

	for word in wordsInRow:
		for letter in word:
			score += lexicon[letter][0]
		wordsInRowAndScores.append((word, score))
		score = 0
	print(wordsInRowAndScores, 'row&score initial formation')

	for word in wordsInColumn:
		for letter in word:
			score += lexicon[letter][0]
		wordsInColumnAndScores.append((word, score))
		score = 0
	print(wordsInColumnAndScores, 'column&score initial formation')

	for move in movesMade:
		for i, wordAndScore in enumerate(wordsInRowAndScores):
			if move[1].getLetter() in wordAndScore[0] and move[1].getScore() == 0:
				wordsInRowAndScores[i] = (wordAndScore[0], (wordAndScore[1]-lexicon[move[1].getLetter()][0]))
	print(wordsInRowAndScores, 'row&score after clearing blanks')

	for move in movesMade:
		for i, wordAndScore in enumerate(wordsInRowAndScores):
			if move[1].getLetter() in wordAndScore[0]:
				match move[2]:
					case 'DL':
						wordsInRowAndScores[i] = (wordAndScore[0], (wordAndScore[1] + move[1].getScore()))
					case 'TL':
						wordsInRowAndScores[i] = (wordAndScore[0], (wordAndScore[1] + 2*move[1].getScore()))
					case _:
						continue
	print(wordsInRowAndScores, 'row&score after letter multipliers')

	for move in movesMade:
		for i, wordAndScore in enumerate(wordsInRowAndScores):
			if move[1].getLetter() in wordAndScore[0]:
				match move[2]:
					case 'DW':
						wordsInRowAndScores[i] = (wordAndScore[0], (wordAndScore[1] * 2))
					case 'TW':
						wordsInRowAndScores[i] = (wordAndScore[0], (wordAndScore[1] * 3))
					case _:
						continue
	print(wordsInRowAndScores, 'row&score after word multipliers')

	for move in movesMade:
		for i, wordAndScore in enumerate(wordsInColumnAndScores):
			if move[1].getLetter() in wordAndScore[0] and move[1].getScore() == 0:
				wordsInColumnAndScores[i] = (wordAndScore[0], (wordAndScore[1] - lexicon[move[1].getLetter()][0]))
	print(wordsInColumnAndScores, 'column&score after clearing blanks')
	for move in movesMade:
		for i, wordAndScore in enumerate(wordsInColumnAndScores):
			if move[1].getLetter() in wordAndScore[0]:
				match move[2]:
					case 'DL':
						wordsInColumnAndScores[i] = (wordAndScore[0], (wordAndScore[1] + move[1].getScore()))
					case 'TL':
						wordsInColumnAndScores[i] = (wordAndScore[0], (wordAndScore[1] + 2 * move[1].getScore()))
					case _:
						continue
	print(wordsInColumnAndScores, 'column&score after letter multipliers')
	for move in movesMade:
		for i, wordAndScore in enumerate(wordsInColumnAndScores):
			if move[1].getLetter() in wordAndScore[0]:
				match move[2]:
					case 'DW':
						wordsInColumnAndScores[i] = (wordAndScore[0], (wordAndScore[1] * 2))
					case 'TW':
						wordsInColumnAndScores[i] = (wordAndScore[0], (wordAndScore[1] * 3))
					case _:
						continue
	print(wordsInColumnAndScores, 'column&score after word multipliers')
	for wordAndScore in wordsInRowAndScores:
		score += wordAndScore[1]

	for wordAndScore in wordsInColumnAndScores:
		score += wordAndScore[1]

	return score


def applyPenalties(player, scoreStolen, lexicon):
	if player.timer.isOvertime:
		scoreToRemove = -10 * (10 - player.timer.current_seconds // 60)
		player.score.updateScore(scoreToRemove)

	if not scoreStolen:
		scoreToRemove = -1 * player.rack.getTotalScore(lexicon)
		player.score.updateScore(scoreToRemove)
	return player


def loadGame(file):
	# try:
	# 	with open(os.path.join(os.path.dirname(__file__), f'../data\\{file}.json')) as f:
	# 		gameData = json.load(f)
	# except FileNotFoundError:
	# 	try:
	# 		with open(os.path.join(os.path.dirname(__file__), f'../data\\{file}')) as f:
	# 			gameData = json.load(f)
	# 	except FileNotFoundError:
	# 		return initialiseScrabbleItems('English', 'Player 1', 'Player 2'), [True, False, False, True, False, 2, False, False, False, 0, False, False, False, False, False, False, False, False, False]

	with open(os.path.join(os.path.dirname(__file__), f'../data\\{file}.json')) as f:
		gameData = json.load(f)

	board = list(gameData['Board'].values())
	print(board)
	gameBoard = ScrabbleItemTemplatesV2.Board((400, 10))
	gameBoard.replaceBoard(board)

	bag = gameData['Tile Bag']['bag']
	language = gameData['Tile Bag']['language']
	TileBag = ScrabbleItemTemplatesV2.TileBag((50, 250), language)
	TileBag.replaceBag(bag)

	for row in range(15):
		for column in range(15):
			if gameBoard.getBoard()[row][column] in TileBag.alphabet:
				tile = ScrabbleItemTemplatesV2.Tile(
					f'{language}Letters\\TILE_{gameBoard.getBoard()[row][column]}.png',
					(448+column*48, 58+row*48),
					gameBoard.getBoard()[row][column],
					TileBag.lexicon[gameBoard.getBoard()[row][column]][0])
				tile.transformImage((32, 32))
				gameBoard.addToGroup(tile)

	TileBag.shuffleCount = 2

	P1Name = gameData['Player 1']['Name']
	P1Rack = gameData['Player 1']['Rack']
	P1Score = gameData['Player 1']['Score']
	P1TimeLeft = gameData['Player 1']['Timer']['Time Left']
	P1Overtime = gameData['Player 1']['Timer']['Overtime']
	Player1 = ScrabbleItemTemplatesV2.Player(P1Name, (550, 775), (1180, 750), (1180, 720))
	Player1.rack.replaceContents(P1Rack)
	Player1.rack.fillRackGroup(language, TileBag.lexicon, (584, 798))
	Player1.score.updateScore(P1Score)
	Player1.timer.current_seconds = P1TimeLeft
	Player1.timer.isOvertime = P1Overtime

	P2Name = gameData['Player 2']['Name']
	P2Rack = gameData['Player 2']['Rack']
	P2Score = gameData['Player 2']['Score']
	P2TimeLeft = gameData['Player 2']['Timer']['Time Left']
	P2Overtime = gameData['Player 2']['Timer']['Overtime']
	Player2 = ScrabbleItemTemplatesV2.Player(P2Name, (550, 775), (1180, 75), (1180, 45))
	Player2.rack.replaceContents(P2Rack)
	Player2.rack.fillRackGroup(language, TileBag.lexicon, (584, 798))
	Player2.score.updateScore(P2Score)
	Player2.timer.current_seconds = P2TimeLeft
	Player2.timer.isOvertime = P2Overtime

	flags = list(gameData['Flags'].values())

	return gameBoard, TileBag, Player1, Player2, flags, P1Name, P2Name


def getPlayerID(username):
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT playerID FROM Players WHERE username=?', (username,))
		userID = cursor.fetchone()
		if userID is not None:
			return userID[0]
		else:
			cursor.execute('''INSERT INTO Players ('username') VALUES (?)''', (username,))
			cursor.execute('SELECT playerID FROM Players WHERE username=?', (username,))
			return cursor.fetchone()[0]


def createGameRecord(adminID, Player1_ID, Player2_ID):
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		current_time = datetime.now()
		cursor.execute('''INSERT INTO Games ('datePlayed') VALUES (?)''', (current_time,))
		cursor.execute('''SELECT gameID FROM Games WHERE datePlayed=?''', (current_time,))
		gameID = cursor.fetchone()[0]
		cursor.execute('''INSERT INTO AdminGames ('gameID', 'adminID') VALUES (?, ?)''', (gameID, adminID,))
		cursor.execute('''INSERT INTO PlayerGames ('gameID', 'playerID') VALUES (?, ?)''', (gameID, Player1_ID,))
		cursor.execute('''INSERT INTO PlayerGames ('gameID', 'playerID') VALUES (?, ?)''', (gameID, Player2_ID,))
		return gameID


def getGameID(filename):
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT gameID FROM Games WHERE fileName=?', (filename,))
		return cursor.fetchone()[0]


def addToGameHistory(gameID, moveNumber, playerID, words, score, exchanged, skipped):
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		cursor.execute('''INSERT INTO GameHistory 
		('gameID', 'moveNumber', 'playerID', 'words', 'score', 'exchanged', 'skipped') 
		VALUES (?, ?, ?, ?, ?, ?, ?)''', (gameID, moveNumber, playerID, words, score, exchanged, skipped,))


# Need to remove entering player names after attempting pg.QUIT. Remove relevant ui elements and flags. ✅
# Also need to display player names during turns and post-game, instead of Player1, Player2. ✅
# Add in text headers for file name and admin password, to explain to users what goes in which box. ✅
# Add in code to retrieve relevant data for the SQL tables, create these functions and put them in at the right locations in the below function


def createGameWindow(adminID='1', P1Name='', P2Name='', newGameLang=None, gameFile=None):

	pg.init()

	# SCREEN_WIDTH = pg.display.Info().current_w
	# SCREEN_HEIGHT = pg.display.Info().current_h

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

	flags = [True, False, False, True, False, 2, False, False, False, 0, False, False, False, False, False, False, False, False, False, 0]

	if newGameLang is not None:
		gameBoard, Player1, Player2, TileBag = initialiseScrabbleItems(newGameLang, P1Name, P2Name)
	elif gameFile is not None:
		gameBoard, TileBag, Player1, Player2, flags, P1Name, P2Name = loadGame(gameFile)
	else:
		gameBoard, Player1, Player2, TileBag = initialiseScrabbleItems('English', P1Name, P2Name)

	Player1_ID = getPlayerID(P1Name)
	Player2_ID = getPlayerID(P2Name)

	print(Player1_ID, 'player1 id')
	print(Player2_ID, 'player2 id')

	if newGameLang is not None:
		gameID = createGameRecord(adminID, Player1_ID, Player2_ID)
	else:
		gameID = getGameID(gameFile)

	print(gameID, 'game id')

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

	enterFileNameLabel = ScrabbleItemTemplatesV2.Text((1252, 300), (200, 50), 'Enter File Name:')

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
		if TileBag.shuffleCount >= 2:
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
					FileNameEntered = True
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
					Player1.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon, (584, 798))
					Player2.rack.fillRack(TileBag)
					Player2.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon, (584, 798))
					readyToStart = True
					fillRack_button.disable()
					PauseButton.enable()

				# if shuffleBag_button has been pressed
				if event.ui_element == shuffleBag_button:
					# Shuffle bag
					TileBag.shuffleBag()

				if event.ui_element == undoMove_button and not (gameOver or isPaused):
					# undo move
					gameBoard, stack, Player1, Player2 = undoPlay(gameBoard, movesMade, Player1_Turn, Player1, Player2, TileBag.getLanguage())

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
											if Player2.rack.isEmpty():
												score += 50
											print(score, 'score for player2')
											Player2.rack.fillRack(TileBag)
											Player2.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon, (584, 798))
											Player2.score.updateScore(score)
										else:
											if Player2.rack.isEmpty():
												scoreToSteal = Player1.rack.getTotalScore(TileBag.lexicon)
												Player2.score.updateScore(scoreToSteal*2)
												gameOver = True
												scoreStolen = True
									else:
										if not TileBag.isEmpty():
											if Player1.rack.isEmpty():
												score += 50
											print(score, 'score for player1')
											Player1.rack.fillRack(TileBag)
											Player1.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon, (584, 798))
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
								sprites[f'TILE{i + 1}'].updateImage(f"{TileBag.getLanguage()}Letters\\TILE_{Player1.rack.getContents()[i]}")
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
			gameWindow.blit(ScrabbleItemTemplatesV2.Text((568, 875), (200, 100), f'{Player1.name}').text, (568, 875))
			# Player1.rack.drawGroup(gameWindow)
			Player1.rack.getGroup().draw(gameWindow)
		elif not Player1_Turn and not gameOver:

			gameWindow.blit(Player2.rack.getImage(), (Player2.rack.getRectCoordinates()))
			gameWindow.blit(ScrabbleItemTemplatesV2.Text((568, 875), (200, 100), f'{Player2.name}').text, (568, 875))
			# Player2.rack.drawGroup(gameWindow)
			Player2.rack.getGroup().draw(gameWindow)

		# Blit the score and timer for both players
		gameWindow.blit(Player1.timer.text, Player1.timer.getRectCoordinates())
		gameWindow.blit(Player1.score.text, Player1.score.getRectCoordinates())

		gameWindow.blit(Player2.timer.text, Player2.timer.getRectCoordinates())
		gameWindow.blit(Player2.score.text, Player2.score.getRectCoordinates())

		if revealOtherRack and Player1_Turn:
			gameWindow.blit(Player2.rack.getImage(), (1050, 775))
			gameWindow.blit(ScrabbleItemTemplatesV2.Text((1068, 875), (200, 100), f'{Player2.name}').text, (1068, 875))
			gameWindow.blit(ScrabbleItemTemplatesV2.Text((568, 875), (200, 100), f'{Player1.name}').text, (568, 875))
			Player2.rack.getGroup().draw(gameWindow)
			gameWindow.blit(Player1.rack.getImage(), Player1.rack.getRectCoordinates())
			Player1.rack.getGroup().draw(gameWindow)
		elif revealOtherRack and not Player1_Turn:
			gameWindow.blit(Player1.rack.getImage(), (1050, 775))
			gameWindow.blit(ScrabbleItemTemplatesV2.Text((1068, 875), (200, 100), f'{Player1.name}').text, (1068, 875))
			gameWindow.blit(ScrabbleItemTemplatesV2.Text((568, 875), (200, 100), f'{Player2.name}').text, (568, 875))
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
