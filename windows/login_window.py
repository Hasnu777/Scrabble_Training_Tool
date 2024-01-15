from windows.windowsTemplate import *
import sqlite3 as sql
from CTkMessagebox import CTkMessagebox
#TODO fix positioning of everything inside the window
LoggedIn = False
username = None
user_id = None


logInWindow = App(1280, 720, 'Log In')
logInWindow.resizable(False, False)

logInLabel = Label(logInWindow, row=430, column=20, padx=10, pady=10, text='Welcome. Please enter details.',
				   font_type='Helvetica', font_size=18)
logInWindow.labels.append(logInLabel)

UsernameEntry = EntryBox(logInWindow, row=440, column=60, padx=15, pady=15, placeholder_text='Enter username')
logInWindow.entries.append(UsernameEntry)

PasswordEntry = EntryBox(logInWindow, row=440, column=100, padx=15, pady=15, placeholder_text='Enter password')
PasswordEntry.entry.configure(show='*')
logInWindow.entries.append(PasswordEntry)

def CreateUser():
	username = UsernameEntry.entry.get()
	password = PasswordEntry.entry.get()
	try:
		with sql.connect('scrabbleTrainingTool.db') as conn:
			conn.cursor().execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
	except sql.IntegrityError:
		CTkMessagebox(title='Error!', message='Username taken.')

CreateUserButton = Button(logInWindow, row=350, column=160, padx=20, pady=20, onclick=CreateUser)
logInWindow.entries.append(CreateUserButton)

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


LogInButton = Button(logInWindow, row=500, column=160, padx=20, pady=20, onclick=LogIn)
logInWindow.entries.append(LogInButton)

def run():
	logInWindow.mainloop()