from windows.windowsTemplate import *
from windows import homescreen_window

def destroyProfileWindow(window, master):
    window.destroy()
    homescreen_window.TopFrame.topLevelWindows['Profile']=None
    unlockFromProfileWindow(master)

def unlockFromProfileWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='normal')

def lockToProfileWindow(master):
    for frame in master.frames.values():
        for button in frame.buttons.values():
            button.configure(state='disabled')

def createProfileWindow(master):
    ProfileWindow = ctk.CTkToplevel(master=master, width=490, height=710)
    ProfileWindow.title('Profile')
    ProfileWindow.protocol("WM_DELETE_WINDOW", lambda: destroyProfileWindow(ProfileWindow, master))
    ProfileFrame = Frame(master=ProfileWindow, width=600, height=400, xpos=0, ypos=0, fg_color='blue')
    TitleLabel = Label(master=ProfileFrame, text='Profile', xpos=10, ypos=10, font_type='Futura', font_size=24)
    ProfileWindow.attributes("-topmost", True)
    lockToProfileWindow(master=master)
    return ProfileWindow
