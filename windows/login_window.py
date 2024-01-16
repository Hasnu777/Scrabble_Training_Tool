from windows.windowsTemplate import *
import sqlite3 as sql
from CTkMessagebox import CTkMessagebox
#TODO fix the function of the checkbox
LoggedIn = False
username = None
user_id = None


logInWindow = App(320, 180, 'Log In')
# logInWindow.resizable(False, False)

logInFrame = Frame(logInWindow, width=320, height=180, xpos=0, ypos=0)
logInFrame.configure(border_width=2, border_color='green')
logInWindow.frames.append(logInFrame)


logInLabel = Label(logInFrame, xpos=3, ypos=5, text='Welcome to the AI Scrabble Trainer 1.0',
				   font_type='Helvetica', font_size=18)
logInFrame.labels.append(logInLabel)


UsernameEntry = EntryBox(logInFrame, xpos=16, ypos=50, placeholder_text='Enter username...')
logInFrame.entries.append(UsernameEntry)

PasswordEntry = EntryBox(logInFrame, xpos=16, ypos=87, placeholder_text='Enter password...')
PasswordEntry.entry.configure(show='*')
logInFrame.entries.append(PasswordEntry)

def show_password():
	if PasswordEntry.entry.cget('show') == '*':
		PasswordEntry.entry.configure(show='')
	else:
		PasswordEntry.entry.configure(show='*')

show_password_entrybox = ctk.CTkCheckBox(logInFrame, border_width=2, onvalue=show_password, offvalue=show_password, text='show password')
show_password_entrybox.place(x=166, y=87)
def CreateUser():
	username = UsernameEntry.entry.get()
	password = PasswordEntry.entry.get()
	try:
		with sql.connect('scrabbleTrainingTool.db') as conn:
			conn.cursor().execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
	except sql.IntegrityError:
		CTkMessagebox(title='Error!', message='Username taken.')

CreateUserButton = Button(logInFrame, button_text='Create User', xpos=166, ypos=135, command=CreateUser)
logInFrame.entries.append(CreateUserButton)

def LogIn():
	usernameEntered = UsernameEntry.entry.get()
	passwordEntered = PasswordEntry.entry.get()

	with sql.connect('scrabbleTrainingTool.db') as conn:
		cur = conn.cursor()
		cur.execute(f"SELECT username FROM users WHERE username='{usernameEntered}' AND password='{passwordEntered}';")
		if not cur.fetchone():
			CTkMessagebox(title='Error!', message='Incorrect username or password given.')
		else:
			logInLabel.label.configure(text='Logged in successfully')
			global LoggedIn
			LoggedIn = True
			global username
			username = usernameEntered
			global user_id
			user_id = cur.execute(f"SELECT id FROM users WHERE username='{username}';").fetchone()[0]
			logInWindow.quit()


LogInButton = Button(logInFrame, button_text='Log In', xpos=16, ypos=135, command=LogIn)
logInFrame.entries.append(LogInButton)

def run():
	logInWindow.mainloop()