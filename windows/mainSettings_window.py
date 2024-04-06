from windows.windowsTemplate import *
from windows import homescreen_window


def destroySettingsWindow(window, master):
    window.destroy()
    homescreen_window.TopFrame.topLevelWindows['Settings']=None
    unlockFromSettingsWindow(master)


def unlockFromSettingsWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='normal')


def lockToSettingsWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='disabled')


def createSettingsWindow(master):
    mainSettingsWindow = ctk.CTkToplevel(master=master, width=600, height=400)
    mainSettingsWindow.title('Settings')
    mainSettingsWindow.protocol("WM_DELETE_WINDOW", lambda: destroySettingsWindow(mainSettingsWindow, master))
    SettingsFrame = Frame(master=mainSettingsWindow, width=600, height=400, xpos=0, ypos=0, fg_color='blue')
    TitleLabel = Label(master=SettingsFrame, text='Settings', xpos=10, ypos=10, font_type='Futura', font_size=24)
    mainSettingsWindow.attributes("-topmost", True)
    lockToSettingsWindow(master=master)
    return mainSettingsWindow
