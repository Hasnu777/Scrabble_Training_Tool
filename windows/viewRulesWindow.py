from windows.windowsTemplate import *
from windows import homescreen_window

def destroyViewRulesWindow(window, master):
    window.destroy()
    homescreen_window.TopFrame.topLevelWindows['viewRulesWindow']=None
    unlockFromViewRulesWindow(master)

def unlockFromViewRulesWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='normal')

def lockToViewRulesWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='disabled')

def createViewRulesWindow(master):
    viewRulesWindow = ctk.CTkToplevel(master=master, width=600, height=400)
    viewRulesWindow.title('View Rules')
    viewRulesWindow.protocol("WM_DELETE_WINDOW", lambda: destroyViewRulesWindow(viewRulesWindow, master))
    viewRulesFrame = Frame(master=viewRulesWindow, width=600, height=400, xpos=0, ypos=0, fg_color='blue')
    TitleLabel = Label(master=viewRulesFrame, text='View Rules', xpos=10, ypos=10, font_type='Futura', font_size=24)
    viewRulesWindow.attributes("-topmost", True)
    lockToViewRulesWindow(master=master)
    return viewRulesWindow
