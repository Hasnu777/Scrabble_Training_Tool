import pygame as pg
import pygame_gui as py_gui
import random
import sqlite3
import os
from gameLogic import ScrabbleItemTemplatesV2


def initialiseScrabbleItems(language):

    gameBoard = ScrabbleItemTemplatesV2.Board((400, 10))
    gameBoard = AddSpecialLocations(gameBoard)

    Player1 = ScrabbleItemTemplatesV2.Player((550, 775), (1180, 750), (1180, 720))

    Player2 = ScrabbleItemTemplatesV2.Player((550, 775), (1180, 75), (1180, 45))

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
    if firstTurn:
        for move in stack:
            validPlay = (move[1].getRectCoordinates() != (784, 394))
        if not validPlay:
            return validPlay, []

    board = gameBoard.getBoard()
    wordsOnBoard = []
    wordsInRow = ''
    for row in board:
        for letter in row:
            if letter in alphabet:
                wordsInRow += letter
            else:
                if language == 'English':
                    if len(wordsInRow) > 1 and wordsInRow not in ('RR', 'LL'):
                        wordsOnBoard.append(wordsInRow)
                else:
                    if len(wordsInRow) > 1 and wordsInRow not in ('CH', 'RR', 'LL'):
                        wordsOnBoard.append(wordsInRow)
                wordsInRow = ''
    if language == 'English':
        if len(wordsInRow) > 1 and wordsInRow not in ('RR', 'LL'):
            wordsOnBoard.append(wordsInRow)
    else:
        if len(wordsInRow) > 1 and wordsInRow not in ('CH', 'RR', 'LL'):
            wordsOnBoard.append(wordsInRow)
    wordsInColumn = ''

    for column in range(15):
        for row in range(15):
            if board[row][column] in alphabet:
                wordsInColumn += board[row][column]
            else:
                if language == 'English':
                    if len(wordsInColumn) > 1 and wordsInColumn not in ('RR', 'LL'):
                        wordsOnBoard.append(wordsInColumn)
                else:
                    if len(wordsInColumn) > 1 and wordsInColumn not in ('CH', 'RR', 'LL'):
                        wordsOnBoard.append(wordsInColumn)
                wordsInColumn = ''
        if language == 'English':
            if len(wordsInColumn) > 1 and wordsInColumn not in ('RR', 'LL'):
                wordsOnBoard.append(wordsInColumn)
        else:
            if len(wordsInColumn) > 1 and wordsInColumn not in ('CH', 'RR', 'LL'):
                wordsOnBoard.append(wordsInColumn)
        wordsInColumn = ''

    wordsCreated = []
    print(wordsOnBoard, 'wordsOnBoard')
    print(wordsPlayed, 'wordsPlayed')
    for word in wordsOnBoard:
        if wordsOnBoard.count(word) > wordsPlayed.count(word):
            for i in range(wordsOnBoard.count(word)-wordsPlayed.count(word)):
                wordsCreated.append(word)
    print(wordsCreated, 'wordsCreated')
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
            tile.transformImage((48, 48))
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
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '../word_lists.db'))
    cursor = conn.cursor()
    for word in wordsToCheck:
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
    tile.updateImage(f'{language}Letters\\TILE_{letter}.png')
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
    player.rack.fillRackGroup(tileBag.getLanguage(), tileBag.lexicon)
    spritesList = player.rack.getSprites()
    newTile = spritesList[f'TILE{tileToExchangePosition+1}']
    print(newTile.getLetter(), 'newTile that was put into rack')
    newTile.canBeClicked = False
    spritesList[f'TILE{tileToExchangePosition+1}'] = newTile
    player.rack.updateSprites(spritesList)
    return player, tileBag, False


def verifyAdminPassword(password):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '../scrabbleTrainingTool.db'))
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE id=1')
    daPassword = cursor.fetchone()
    print(daPassword)
    if password == daPassword[0]:
        return True


def calculateScore():
    pass


def createGameWindow(language):

    pg.init()

    # SCREEN_WIDTH = pg.display.Info().current_w
    # SCREEN_HEIGHT = pg.display.Info().current_h

    pg.display.set_caption('Scrabble Tournament Game')
    gameWindow = pg.display.set_mode((1600, 900))

    gameBoard, Player1, Player2, TileBag = initialiseScrabbleItems(language)

    background = pg.Surface((1600, 900))
    background.fill(pg.Color('#006a00'))

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

    exchangeTile_button = py_gui.elements.UIButton(relative_rect=pg.Rect((218, 800), (100, 50)), text='Exchange Tile', manager=UIManager)

    pg.time.set_timer(pg.USEREVENT, 1000)

    running = True

    Player1_Turn = True

    orderDetermined = False
    readyToStart = False
    firstTurn = True
    invalidPlay = False
    blankTilesInPlay = 2
    mustSwapBlank = False
    blankTileClicked = False
    exchangeOccurring = False
    consecutiveZeroPointPlays = 0

    getLetterToReplace = py_gui.elements.UIWindow(pg.Rect(1210, 338, 400, 300), manager=UIManager, window_display_title='New Letter?')
    getLetterToReplace.hide()

    selectLetterToReplace = py_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=TileBag.alphabet[1:], starting_option='A', relative_rect=pg.Rect((1210, 338), (50, 20)), manager=UIManager)
    selectLetterToReplace.hide()

    getAdminPassword = py_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pg.Rect((1250, 400), (200, 30)), manager=UIManager)
    getAdminPassword.disable()
    getAdminPassword.hide()

    enterAdminPassword = py_gui.elements.UIButton(relative_rect=pg.Rect((1460, 400), (75, 20)),  text='Enter', manager=UIManager, text_kwargs={'size': '4'})
    enterAdminPassword.hide()

    gameOver = False

    # getLetterToReplace = py_gui.elements.UIWindow(pg.Rect(SCREEN_WIDTH/2-200, SCREEN_HEIGHT/2-150, 400, 300), manager=UIManager, window_display_title='WARNING')

    invalidPlayWarning = ScrabbleItemTemplatesV2.Text((1210, 338), (200, 100), 'Invalid Play. Try again.')

    movesMade = []  # stack :D
    wordsPlayed = []

    Player1TileClicked = False
    Player2TileClicked = False

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
                if getAdminPassword.is_enabled == 0:
                    getAdminPassword.show()
                    getAdminPassword.enable()
                    enterAdminPassword.show()
                    print('enabled da password ting')
                if event.type == pg.QUIT:
                    if getAdminPassword.is_enabled == 0:
                        getAdminPassword.show()
                        getAdminPassword.enable()

                if event.type == py_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == enterAdminPassword:
                        print('button has been pressed')
                        correctPasswordEntered = verifyAdminPassword(getAdminPassword.get_text())
                        if correctPasswordEntered:
                            running = False
                            break

                if event.type == py_gui.UI_TEXT_ENTRY_FINISHED:
                    correctPasswordEntered = verifyAdminPassword(getAdminPassword.get_text())
                    if correctPasswordEntered:
                        running = False
                        break

            # if user closes the window
            if event.type == pg.QUIT:
                running = False
                break

            # if a pygame_gui button has been pressed
            if event.type == py_gui.UI_BUTTON_PRESSED:

                if event.ui_element == exchangeTile_button and (Player1TileClicked or Player2TileClicked):
                    print('exchange button clicked')
                    if Player1TileClicked:
                        print('player 1 initiating exchange')
                        Player1, TileBag, Player1TileClicked = findTileToExchange(Player1, TileBag)
                    else:
                        Player2, TileBag, Player2TileClicked = findTileToExchange(Player2, TileBag)
                    exchangeOccurring = True

                # if fillRack_button has been pressed
                if event.ui_element == fillRack_button and TileBag.shuffleCount >= 2:
                    Player1.rack.fillRack(TileBag)
                    Player1.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)
                    Player2.rack.fillRack(TileBag)
                    Player2.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)
                    readyToStart = True
                    fillRack_button.disable()

                # if shuffleBag_button has been pressed
                if event.ui_element == shuffleBag_button:
                    TileBag.shuffleBag()

                if event.ui_element == undoMove_button:
                    gameBoard, stack, Player1, Player2 = undoPlay(gameBoard, movesMade, Player1_Turn, Player1, Player2, TileBag.getLanguage())

                # if swapTurn_button has been pressed
                if event.ui_element == swapTurn_button and TileBag.shuffleCount >= 2:
                    if not exchangeOccurring:  # check board now
                        valid, wordsCreated = checkTurn(gameBoard, movesMade, TileBag.getLanguage(), TileBag.alphabet, firstTurn, wordsPlayed)
                        print(wordsCreated, 'wordsCreated')
                        if wordsCreated:
                            valid = checkWords(wordsCreated, TileBag.getLanguage())
                            if valid:  # need to code in awarding the score
                                print('valid turn')
                                Player1_Turn = not Player1_Turn
                                if Player1_Turn:
                                    Player2.rack.fillRack(TileBag)
                                    Player2.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)
                                else:
                                    Player1.rack.fillRack(TileBag)
                                    Player1.rack.fillRackGroup(TileBag.getLanguage(), TileBag.lexicon)
                                invalidPlay = False
                                print(movesMade)
                                movesMade = []
                                for word in wordsCreated:
                                    wordsPlayed.append(word)
                                consecutiveZeroPointPlays = 0
                            else:
                                gameBoard, stack, Player1, Player2 = undoPlay(gameBoard, movesMade, Player1_Turn, Player1, Player2, TileBag.getLanguage())
                                invalidPlay = True
                                print('invalid turn')  # need to code in the user being informed their play was invalid, and their moves being undone
                            print('Turn swapped')
                            print(movesMade, 'stack')
                            print(wordsPlayed, 'wordsPlayed')
                        else:
                            Player1_Turn = not Player1_Turn
                            consecutiveZeroPointPlays += 1
                    else:
                        Player1_Turn = not Player1_Turn
                        consecutiveZeroPointPlays += 1
                        exchangeOccurring = False

                # If determineOrder_button has been pressed
                if event.ui_element == determineOrder_button:
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
            if event.type == pg.USEREVENT and readyToStart:
                if Player1.timer.current_seconds != 0 and Player1_Turn and not gameOver:
                    Player1.timer.current_seconds -= 1
                    Player1.timer.updateTimer()
                    if consecutiveZeroPointPlays == 6:
                        gameOver = True
                    if Player1.timer.current_seconds == 0 and not Player1.timer.isOvertime and not gameOver:
                        Player1.replaceTimer()
                    elif Player1.timer.current_seconds == 0 and Player1.timer.isOvertime:
                        gameOver = True

                if Player2.timer.current_seconds != 0 and not Player1_Turn and not gameOver:
                    Player2.timer.current_seconds -= 1
                    Player2.timer.updateTimer()
                    if consecutiveZeroPointPlays == 6:
                        gameOver = True
                    if Player2.timer.current_seconds == 0 and not Player2.timer.isOvertime and not gameOver:
                        Player2.replaceTimer()
                    elif Player2.timer.current_seconds == 0 and Player2.timer.isOvertime:
                        gameOver = True

            # if event.type == pg.USEREVENT and blankTileClicked:
            if event.type == py_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == selectLetterToReplace:
                    movesMade, blankTileClicked, gameBoard = swapBlankToLetter(movesMade, event.text, TileBag.getLanguage(), gameBoard)
                    blankTilesInPlay -= 1
                    selectLetterToReplace.disable()
                    selectLetterToReplace.hide()
                    blankTileClicked = False
                    mustSwapBlank = False

            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
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

        # if consecutiveZeroPointPlays == 6 or gameOver:
        #     print('game over: 6 consecutive zero-point-scoring plays have occurred')
        #     if getAdminPassword.is_enabled == 0:
        #         getAdminPassword.show()
        #         getAdminPassword.enable()
        #         print('enabled da password ting')
        #     print('brudda wot')
        #     for event in pg.event.get():
        #         print('broski please')
        #         if event.type == pg.QUIT:
        #             if getAdminPassword.is_enabled == 0:
        #                 getAdminPassword.show()
        #                 getAdminPassword.enable()
        #
        #         if event.type == py_gui.UI_TEXT_ENTRY_FINISHED:
        #             correctPasswordEntered = verifyAdminPassword(getAdminPassword.get_text())
        #             if correctPasswordEntered:
        #                 running = False
        #                 break

        # Update game window, draw background, and draw buttons
        UIManager.update(time_delta)
        gameWindow.blit(background, (0, 0))
        UIManager.draw_ui(gameWindow)

        # Blit the board and tile bag
        gameWindow.blit(gameBoard.getImage(), (gameBoard.getRectCoordinates()))
        gameWindow.blit(TileBag.getImage(), (TileBag.getRectCoordinates()))

        # Blit the rack and tiles for whose turn it is
        if Player1_Turn:
            gameWindow.blit(Player1.rack.getImage(), (Player1.rack.getRectCoordinates()))
            # Player1.rack.drawGroup(gameWindow)
            Player1.rack.getGroup().draw(gameWindow)
        else:

            gameWindow.blit(Player2.rack.getImage(), (Player2.rack.getRectCoordinates()))
            # Player2.rack.drawGroup(gameWindow)
            Player2.rack.getGroup().draw(gameWindow)

        # Blit the score and timer for both players
        gameWindow.blit(Player1.timer.text, Player1.timer.getRectCoordinates())
        gameWindow.blit(Player1.score.text, Player1.score.getRectCoordinates())

        gameWindow.blit(Player2.timer.text, Player2.timer.getRectCoordinates())
        gameWindow.blit(Player2.score.text, Player2.score.getRectCoordinates())

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
