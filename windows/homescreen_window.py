from windows.windowsTemplate import *
from windows import viewProfile_window, mainSettings_window, createNewGameSettings, loadGame, viewSavedGamesWindow, viewRulesWindow, viewDictionaryWindow
from PIL import Image
import os

# TODO complete TopFrame and finish homescreen window

homescreen = App(width=1280, height=720, title='AI Scrabble Trainer')


'''
Creating Top Section of Window
'''


TopFrame = Frame(master=homescreen, width=1280, height=72, xpos=0, ypos=0, fg_color='green')
homescreen.frames['TopFrame'] = TopFrame

UserProfileIconImage = Image.open(os.path.join(os.path.dirname(__file__), 'assets\\UserProfileIcon.png'))
UserProfileIcon = ctk.CTkImage(light_image=UserProfileIconImage, dark_image=UserProfileIconImage)
UserProfileIcon.configure(size=(40, 40))
TopFrame.images['UserProfileIcon'] = UserProfileIcon


def viewProfile():
    if TopFrame.topLevelWindows['Profile'] is None:
        TopFrame.topLevelWindows['Profile'] = viewProfile_window.createProfileWindow(homescreen)


TopFrame.topLevelWindows['Profile'] = None
ProfileButton = Button(master=TopFrame, button_text='View Profile', button_image=UserProfileIcon, width=60, height=60,
                       xpos=3, ypos=3, command=viewProfile, compound="top")
ProfileButton.configure(font=('Georgia', 8))
TopFrame.buttons['ProfileButton'] = ProfileButton


SettingsIconImage = Image.open(os.path.join(os.path.dirname(__file__), 'assets\\SettingsIcon.png'))
SettingsIcon = ctk.CTkImage(light_image=SettingsIconImage, dark_image=SettingsIconImage)
SettingsIcon.configure(size=(40, 40))
TopFrame.images['SettingsIcon'] = SettingsIcon


def viewSettings():
    if TopFrame.topLevelWindows['Settings'] is None:
        TopFrame.topLevelWindows['Settings'] = mainSettings_window.createSettingsWindow(homescreen)


TopFrame.topLevelWindows['Settings'] = None
SettingsButton = Button(master=TopFrame, button_text='View Settings', button_image=SettingsIcon, width=60, height=60,
                        xpos=1207, ypos=3, command=viewSettings, compound='top')
SettingsButton.configure(font=('Georgia', 8))
TopFrame.buttons['SettingsButton'] = SettingsButton



'''
Creating Main Section of Window
'''


MainFrame = Frame(master=homescreen, width=1280, height=576, xpos=0, ypos=73, fg_color='blue')
homescreen.frames['MainFrame'] = MainFrame

NewGameSettingsIconImage = Image.open(os.path.join(os.path.dirname(__file__), 'assets\\NewGameSettingsIcon.png'))
NewGameSettingsImage = ctk.CTkImage(light_image=NewGameSettingsIconImage, dark_image=NewGameSettingsIconImage)
NewGameSettingsImage.configure(size=(200, 200))
MainFrame.images['NewGameSettingsIcon'] = NewGameSettingsImage


def NewGame():
    if MainFrame.topLevelWindows['newGameSettings'] is None:
        MainFrame.topLevelWindows['newGameSettings'] = createNewGameSettings.createNewGameSettingsWindow(homescreen)


MainFrame.topLevelWindows['newGameSettings'] = None
newGameSettingsButton = Button(master=MainFrame, button_text='', button_image=NewGameSettingsImage, width=200, height=200, xpos=300, ypos=200, command=NewGame)
MainFrame.buttons['NewGameSettingsButton'] = newGameSettingsButton

LoadGameIconImage = Image.open(os.path.join(os.path.dirname(__file__), 'assets\\LoadGameIcon.png'))
LoadGameIcon = ctk.CTkImage(light_image=LoadGameIconImage, dark_image=LoadGameIconImage)
LoadGameIcon.configure(size=(200, 200))
MainFrame.images['LoadGameIcon'] = LoadGameIcon


def LoadGame():
    if MainFrame.topLevelWindows['LoadGame'] is None:
        MainFrame.topLevelWindows['LoadGame'] = loadGame.createLoadGameWindow(homescreen)


MainFrame.topLevelWindows['LoadGame'] = None
LoadGameButton = Button(master=MainFrame, button_text='', button_image=LoadGameIcon, width=200, height=200, xpos=550, ypos=200, command=LoadGame)
MainFrame.buttons['LoadGameButton']=LoadGameButton

ViewSavedGamesIconImage = Image.open(os.path.join(os.path.dirname(__file__), 'assets\\ViewSavedGamesIcon.png'))
ViewSavedGamesIcon = ctk.CTkImage(light_image=ViewSavedGamesIconImage, dark_image=ViewSavedGamesIconImage)
ViewSavedGamesIcon.configure(size=(200,200))
MainFrame.images['ViewSavedGamesIcon']=ViewSavedGamesIcon

def ViewSavedGames():
    if MainFrame.topLevelWindows['viewSavedGames'] is None:
        MainFrame.topLevelWindows['viewSavedGames'] = viewSavedGamesWindow.createViewSavedGamesWindow(homescreen)

MainFrame.topLevelWindows['viewSavedGames'] = None
ViewSavedGamesButton = Button(master=MainFrame, button_text='', button_image=ViewSavedGamesIcon, width=200, height=200, xpos=800, ypos=200, command=ViewSavedGames)
MainFrame.buttons['ViewSavedGamesButton']=ViewSavedGamesButton

'''
Creating Bottom Section of Window
'''

BottomFrame = Frame(master=homescreen, width=1280, height=72, xpos=0, ypos=648, fg_color='green')
homescreen.frames['BottomFrame']=BottomFrame

RulesIconImage = Image.open(os.path.join(os.path.dirname(__file__), 'assets\\RulesIcon.png'))
RulesIcon = ctk.CTkImage(light_image=RulesIconImage, dark_image=RulesIconImage)
RulesIcon.configure(size=(40, 40))
BottomFrame.images['RulesIcon'] = RulesIcon


def viewRules():
    if BottomFrame.topLevelWindows['viewRulesWindow'] is None:
        BottomFrame.topLevelWindows['viewRulesWindow'] = viewRulesWindow.createViewRulesWindow(homescreen)


BottomFrame.topLevelWindows['viewRulesWindow'] = None
ViewRulesButton = Button(master=BottomFrame, button_text='View Rules', button_image=RulesIcon, width=60, height=60, xpos=3, ypos=0, command=viewRules, compound='top')
BottomFrame.buttons['ViewRulesButton']=ViewRulesButton

DictionaryIconImage = Image.open(os.path.join(os.path.dirname(__file__), 'assets\\DictionaryIcon.png'))
DictionaryIcon = ctk.CTkImage(light_image=DictionaryIconImage, dark_image=DictionaryIconImage)
DictionaryIcon.configure(size=(40,40))
BottomFrame.images['DictionaryIcon']=DictionaryIcon


def viewDictionary():
    if BottomFrame.topLevelWindows['viewDictionaryWindow'] is None:
        BottomFrame.topLevelWindows['viewDictionaryWindow'] = viewDictionaryWindow.createViewDictionaryWindow(homescreen)


BottomFrame.topLevelWindows['viewDictionaryWindow'] = None
ViewDictionaryButton = Button(master=BottomFrame, button_text='View Dictionary', button_image=DictionaryIcon, width=60, height=60, xpos=84, ypos=0, command=viewDictionary, compound='top')
BottomFrame.buttons['ViewDictionaryButton'] = ViewDictionaryButton

GameVersion = Label(master=BottomFrame, xpos=1150, ypos=36, text='Version 1.0', font_type='Helvetica', font_size=24, fg_color='blue', text_color='green')
BottomFrame.labels['GameVersion']=GameVersion



def run():
    homescreen.mainloop()

#TODO once profile and settings windows are made, need to make it so buttons are disabled so long as those windows are open. OR: just re-direct user back to that window.