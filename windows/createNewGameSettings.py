#TODO figure out if the filename should be changed to 'createNewGame' or 'newGame'

from windows.windowsTemplate import *
from windows import homescreen_window

def destroyNewGameSettingsWindow(window, master):
    window.destroy()
    homescreen_window.TopFrame.topLevelWindows['newGameSettings']=None
    unlockFromNewGameSettingsWindow(master)

def unlockFromNewGameSettingsWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='normal')

def lockToNewGameSettingsWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='disabled')

def createNewGameSettingsWindow(master):
    newGameSettingsWindow = ctk.CTkToplevel(master=master, width=600, height=400)
    newGameSettingsWindow.title('Create New Game')
    newGameSettingsWindow.protocol("WM_DELETE_WINDOW", lambda: destroyNewGameSettingsWindow(newGameSettingsWindow, master))
    newGameSettingsFrame = Frame(master=newGameSettingsWindow, width=600, height=400, xpos=0, ypos=0, fg_color='blue')
    TitleLabel = Label(master=newGameSettingsFrame, text='Create New Game', xpos=10, ypos=10, font_type='Futura', font_size=24)
    newGameSettingsWindow.attributes("-topmost", True)
    lockToNewGameSettingsWindow(master=master)
    return newGameSettingsWindow
