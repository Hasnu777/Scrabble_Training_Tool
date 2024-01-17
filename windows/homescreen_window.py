from windowsTemplate import *
from PIL import Image

#TODO complete TopFrame and finish homescreen window

homescreen = App(width=1600, height=900, title='AI Scrabble Trainer')

TopFrame = Frame(master=homescreen, width=1590, height=90, xpos=5, ypos=5, fg_color='green')
homescreen.frames.append(TopFrame)
UserProfileIconImage = Image.open('assets/UserProfileIcon.png')
UserProfileIcon = ctk.CTkImage(light_image=UserProfileIconImage, dark_image=UserProfileIconImage)
UserProfileIcon.configure(size=(40, 40))

def viewProfile():
	print('test complete')

ProfileButton = Button(master=TopFrame, button_text='View Profile', button_image=UserProfileIcon, width=80, height=80, xpos=5, ypos=5, command=viewProfile, compound="top")
ProfileButton.configure(font=('Georgia', 14))




homescreen.mainloop()