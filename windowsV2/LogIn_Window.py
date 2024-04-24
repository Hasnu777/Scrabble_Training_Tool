import sqlite3 as sql
from CTkMessagebox import CTkMessagebox
import os
import customtkinter as ctk

'''Important Variables'''
LoggedIn = False
adminID = None

# Creating the log in window and calibrating it
logInWindow = ctk.CTk()
logInWindow.title('Log In')
logInWindow.geometry(f"320x180+{logInWindow.winfo_screenwidth()//2 - 160}+{logInWindow.winfo_screenheight()//2 - 90}")
logInWindow.resizable(False, False)


# Used to kill the login window after the user closes it, e.g. clicking the close button or pressing Alt+F4
def destroy():
	logInWindow.wm_withdraw()
	logInWindow.quit()
	logInWindow.destroy()


# Defining what to do when a user attempts to close the login window
logInWindow.protocol("WM_DELETE_WINDOW", destroy)

# Creating & placing a label for the window, to explain its purpose
mainText = ctk.CTkLabel(logInWindow, text='Enter administrator details below', font=('Helvetica', 16))
mainText.place(x=5, y=5,)

# Creating the entry boxes to get the username and password
UsernameEntry = ctk.CTkEntry(logInWindow, placeholder_text='Username')
UsernameEntry.place(x=16, y=50)
PasswordEntry = ctk.CTkEntry(logInWindow, placeholder_text='Password')
PasswordEntry.place(x=16, y=87)
PasswordEntry.configure(show='*')  # Password protection, to prevent peeping players from getting the password


# Used to control whether the password is shown as asterisks or in plaintext
def showPassword():
	if showPassword_var.get() == '':
		PasswordEntry.configure(show='')
	else:
		PasswordEntry.configure(show='*')


# Creating the checkbox to show the password
showPassword_var = ctk.StringVar(value='*')
showPasswordCheckBox = ctk.CTkCheckBox(logInWindow, border_width=2, command=showPassword,
										variable=showPassword_var, onvalue='', offvalue='*', text='Show Password')
showPasswordCheckBox.place(x=166, y=89)


def CreateUser():
	usernameEntered = UsernameEntry.get()  # Retrieves username from the textbox
	passwordEntered = PasswordEntry.get()  # Retrieves password from the textbox
	# Checking if the username entered contains characters not from A-Z, a-z, 0-9
	if not (usernameEntered.isalnum() or usernameEntered.isalpha()):
		# Message box created to inform the user of the invalid input
		CTkMessagebox(title='Input Error', message='Invalid username provided for user creation.', width=160, height=80,
					sound=True)
		validUsername = False
	# Minimum username length required, so that all administrator usernames are long enough to be recognisable
	elif len(usernameEntered) < 6:
		# Message box created to inform the user of the invalid input
		CTkMessagebox(title='Input Error', message='Username must be at least 6 characters in length.', width=160,
					height=80, sound=True)
		validUsername = False
	else:  # If the username meets the requirements
		validUsername = True

	if len(passwordEntered) < 8:  # Minimum password length makes it harder for players to penetrate the system
		CTkMessagebox(title='Input Error', message='Password must be at least 8 characters in length.', width=160,
					height=80, sound=True)
		validPassword = False
	else:  # If the password meets the length requirement
		validPassword = True

	if validUsername and validPassword:  # If both username and password are valid
		try:
			# Opening SQL connection to database
			with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
				cursor = conn.cursor()
				# Creates a record for the new administrator profile
				cursor.execute('''INSERT INTO Administrators ('username', 'password') VALUES (?, ?)''',
					(usernameEntered, passwordEntered,))
				cursor.execute('''SELECT adminID FROM Administrators WHERE username=?''',
					(usernameEntered,))  # Retrieves the adminID of the newly created administrator profile
				CTkMessagebox(title='Success!', message='Profile Successfully Created', width=160, height=80,
							sound=True)
		except sql.IntegrityError:  # In case a record with the username already exists
			# Informs the user that the username is taken
			CTkMessagebox(title='Error!', message='Username taken.', width=160, height=80, sound=True)


# Button that executes the CreateUser() subroutine
CreateUser_Button = ctk.CTkButton(logInWindow, text='Create User', command=CreateUser)
CreateUser_Button.place(x=166, y=135)


def LogIn():
	usernameEntered = UsernameEntry.get()  # Retrieves username from the textbox
	passwordEntered = PasswordEntry.get()  # Retrieves password from the textbox
	# Opening connection to database, automatically closes after completing execution of indented code
	with sql.connect(os.path.join(os.path.dirname(__file__), '../ScrabbleTournamentGame.db')) as conn:
		cursor = conn.cursor()
		cursor.execute('''SELECT adminID FROM Administrators WHERE username=? and password=?''',
			(usernameEntered, passwordEntered))  # Retrieving adminID of user who has logged in
		itemsRetrieved = cursor.fetchone()  # Retrieves what was fetched from the SQL query
		if not itemsRetrieved:  # Checks if there was no adminID pulled out (itemsRetrieved would be None in that case)
			# Informs the user that the details provided are invalid
			CTkMessagebox(title='Error!', message='Incorrect username or password given.', width=160, height=80,
						sound=True)
		else:
			global LoggedIn, adminID
			LoggedIn = True
			adminID = itemsRetrieved[0]  # Assigns retrieved adminID
			destroy()  # Kills the window after an administrator has logged in


# Button that executes the LogIn() subroutine
LogIn_Button = ctk.CTkButton(logInWindow, text='Log In', command=LogIn)
LogIn_Button.place(x=16, y=135)


def run():
	logInWindow.mainloop()  # Runs the window
	return adminID
