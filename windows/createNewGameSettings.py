#TODO figure out if the filename should be changed to 'createNewGame' or 'newGame'

from windows.windowsTemplate import *
from windows import homescreen_window
import customtkinter as ctk

LanguageOptions = None
lang = ''
masterWindow = None
NewGameWindow = None
def destroyNewGameSettingsWindow(window, master):
    window.destroy()
    homescreen_window.MainFrame.topLevelWindows['newGameSettings'] = None
    unlockFromNewGameSettingsWindow(master)


def unlockFromNewGameSettingsWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='normal')


def lockToNewGameSettingsWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='disabled')


def getLanguageOption():
    global LanguageOptions, lang
    lang = LanguageOptions.get()
    destroyNewGameSettingsWindow(NewGameWindow, masterWindow)
    masterWindow.destroy()


def createNewGameSettingsWindow(master):
    global masterWindow, NewGameWindow
    masterWindow = master

    NewGameWindow = ctk.CTkToplevel(master=masterWindow, width=600, height=400)
    NewGameWindow.title('Create New Game')
    NewGameWindow.protocol("WM_DELETE_WINDOW", lambda: destroyNewGameSettingsWindow(NewGameWindow, master))
    newGameSettingsFrame = Frame(master=NewGameWindow, width=600, height=400, xpos=0, ypos=0, fg_color='blue')
    TitleLabel = Label(master=newGameSettingsFrame, text='Create New Game', xpos=10, ypos=10, font_type='Futura', font_size=24)
    getLanguageOptionButton = Button(master=newGameSettingsFrame, button_text='Enter', command=getLanguageOption, xpos=250, ypos=100)
    global LanguageOptions
    LanguageOptions = ctk.CTkComboBox(master=newGameSettingsFrame, values=['English', 'French', 'Spanish'])
    LanguageOptions.place(x=100, y=100)
    LanguageOptions.set('English')
    NewGameWindow.attributes("-topmost", True)
    lockToNewGameSettingsWindow(master=masterWindow)
    return NewGameWindow
