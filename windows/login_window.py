from windows.windowsTemplate import *
import sqlite3 as sql
from CTkMessagebox import CTkMessagebox


LoggedIn = False
username = None
user_id = None

logInWindow = App(320, 180, 'Log In')
logInWindow.resizable(False, False)

def destroy_logInWindow():
	logInWindow.quit()
	#TODO stop the above line from causing error and stopping launch of homescreen_window


logInWindow.protocol("WM_DELETE_WINDOW", destroy_logInWindow)


logInFrame = Frame(logInWindow, width=320, height=180, xpos=0, ypos=0)
logInFrame.configure(border_width=2, border_color='green')
logInWindow.frames['logInFrame']=logInFrame

logInLabel = Label(logInFrame, xpos=3, ypos=5, text='Welcome to the AI Scrabble Trainer 1.0',
				   font_type='Helvetica', font_size=18)
logInFrame.labels['logInLabel']=logInLabel

UsernameEntry = EntryBox(logInFrame, xpos=16, ypos=50, placeholder_text='Enter username...')
logInFrame.entries['UsernameEntry']=UsernameEntry

PasswordEntry = EntryBox(logInFrame, xpos=16, ypos=87, placeholder_text='Enter password...')
PasswordEntry.entry.configure(show='*')
logInFrame.entries['PasswordEntry']=PasswordEntry


def show_password():
	if show_password_check_var.get() == '':
		PasswordEntry.entry.configure(show='')
	else:
		PasswordEntry.entry.configure(show='*')

show_password_check_var = ctk.StringVar(value='*')
show_password_entrybox = ctk.CTkCheckBox(logInFrame, border_width=2, command=show_password, variable=show_password_check_var, onvalue='', offvalue='*',
										 text='show password')
show_password_entrybox.place(x=166, y=87)


def CreateUser():
	usernameGiven = UsernameEntry.entry.get()
	password = PasswordEntry.entry.get()

	if len(usernameGiven) != 0:
		try:
			with sql.connect('scrabbleTrainingTool.db') as conn:
				conn.cursor().execute(f"INSERT INTO users (username, password) VALUES ('{usernameGiven}', '{password}')")
		except sql.IntegrityError:
			CTkMessagebox(title='Error!', message='Username taken.')
	else:
		CTkMessagebox(title='Error', message='Invalid username provided.')


CreateUserButton = Button(logInFrame, button_text='Create User', xpos=166, ypos=135, command=CreateUser)
logInFrame.entries['CreateUserButton']=CreateUserButton


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
			destroy_logInWindow()


LogInButton = Button(logInFrame, button_text='Log In', xpos=16, ypos=135, command=LogIn)
logInFrame.entries['LogInButton']=LogInButton


def run():
	logInWindow.mainloop()
	logInWindow.destroy()
	return user_id, username
