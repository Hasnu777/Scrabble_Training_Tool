import sqlite3


def create_profiles_table():
	conn = sqlite3.connect('scrabbleTrainingTool.db')
	cursor = conn.cursor()

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT NOT NULL UNIQUE,
			password TEXT
	)
	''')

	conn.commit()
	conn.close()

#create_profiles_table()

