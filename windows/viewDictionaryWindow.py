from windows.windowsTemplate import *
from windows import homescreen_window


def destroyViewDictionaryWindow(window, master):
    window.destroy()
    homescreen_window.BottomFrame.topLevelWindows['viewDictionaryWindow'] = None
    unlockFromViewDictionaryWindow(master)


def unlockFromViewDictionaryWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='normal')


def lockToViewDictionaryWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='disabled')


def createViewDictionaryWindow(master):
    viewDictionaryWindow = ctk.CTkToplevel(master=master, width=600, height=400)
    viewDictionaryWindow.title('View Dictionary')
    viewDictionaryWindow.protocol("WM_DELETE_WINDOW", lambda: destroyViewDictionaryWindow(viewDictionaryWindow, master))
    viewDictionaryFrame = Frame(master=viewDictionaryWindow, width=600, height=400, xpos=0, ypos=0, fg_color='blue')
    TitleLabel = Label(master=viewDictionaryFrame, text='View Dictionary', xpos=10, ypos=10, font_type='Futura', font_size=24)
    viewDictionaryWindow.attributes("-topmost", True)
    lockToViewDictionaryWindow(master=master)
    return viewDictionaryWindow
