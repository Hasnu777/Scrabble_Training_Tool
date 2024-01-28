#TODO this is a note: Alex n Liam said I should allow multiple unfinished games to be saved, and have them be loadable.
# So, do I rebrand the continueGame thing into loadGame?

from windows.windowsTemplate import *
from windows import homescreen_window

def destroyLoadGame(window, master):
    window.destroy()
    homescreen_window.TopFrame.topLevelWindows['LoadGame']=None
    unlockFromLoadGameWindow(master)

def unlockFromLoadGameWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='normal')

def lockToLoadGameWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='disabled')

def createLoadGameWindow(master):
    LoadGameWindow = ctk.CTkToplevel(master=master, width=600, height=400)
    LoadGameWindow.title('Load Game')
    LoadGameWindow.protocol("WM_DELETE_WINDOW", lambda: destroyLoadGame(LoadGameWindow, master))
    LoadGameFrame = Frame(master=LoadGameWindow, width=600, height=400, xpos=0, ypos=0, fg_color='blue')
    TitleLabel = Label(master=LoadGameFrame, text='Load Game', xpos=10, ypos=10, font_type='Futura', font_size=24)
    LoadGameWindow.attributes("-topmost", True)
    lockToLoadGameWindow(master=master)
    return LoadGameWindow
