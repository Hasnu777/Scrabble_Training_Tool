from windows.windowsTemplate import *
from windows import homescreen_window

def destroyViewSavedGamesWindow(window, master):
    window.destroy()
    homescreen_window.MainFrame.topLevelWindows['viewSavedGames']=None
    unlockFromViewSavedGamesWindow(master)

def unlockFromViewSavedGamesWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='normal')

def lockToViewSavedGamesWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='disabled')

def createViewSavedGamesWindow(master):
    viewSavedGamesWindow = ctk.CTkToplevel(master=master, width=600, height=400)
    viewSavedGamesWindow.title('View Saved Games')
    viewSavedGamesWindow.protocol("WM_DELETE_WINDOW", lambda: destroyViewSavedGamesWindow(viewSavedGamesWindow, master))
    viewSavedGamesFrame = Frame(master=viewSavedGamesWindow, width=600, height=400, xpos=0, ypos=0, fg_color='blue')
    TitleLabel = Label(master=viewSavedGamesFrame, text='View Saved Games', xpos=10, ypos=10, font_type='Futura', font_size=24)
    viewSavedGamesWindow.attributes("-topmost", True)
    lockToViewSavedGamesWindow(master=master)
    return viewSavedGamesWindow
