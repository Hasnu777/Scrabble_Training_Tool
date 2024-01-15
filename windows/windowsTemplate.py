import customtkinter as ctk
import CTkMessagebox


# TODO convert these classes to inherit the ctk.class stuff and then mess with the constructor to fix any errors

class App(ctk.CTk):
	def __init__(self, width, height, title, icon=None):
		super().__init__()
		self.geometry(f'{width}x{height}')
		self.resizable(True, True)
		self.title(title)
		self.buttons = []
		self.labels = []
		self.entries = []
		ctk.set_appearance_mode('System')
		ctk.set_default_color_theme('dark-blue')
		if icon is not None:
			self.iconbitmap(icon)


class Button:
	def __init__(self, window, row=0, column=0, padx=0, pady=0, onclick=None):
		self.command = onclick
		self.button = ctk.CTkButton(window, command=self.command)
		self.button.grid(row=row, column=column, padx=padx, pady=pady)


class Label():
	def __init__(self, window, row=10, column=10, padx=10, pady=10, text='', font_type='Georgia', font_size=24,
				 fg_color='transparent', text_color='blue'):
		self.label = ctk.CTkLabel(window, text=text, font=(font_type, font_size))
		self.label.grid(row=row, column=column, padx=padx, pady=pady)
		self.text = text
		self.font = (font_type, font_size)
		self.fg_color = fg_color
		self.text_color = text_color

	def update_label(self):
		self.label.configure(text='okay never mind', text_color='green', font=self.font)
		print('OY MY GOD')


class EntryBox():
	def __init__(self,
				 window,
				 placeholder_text='Enter text',
				 row=100,
				 column=100,
				 padx=10,
				 pady=10
				 ):
		self.entry = ctk.CTkEntry(window, placeholder_text=placeholder_text)
		self.entry.grid(row=row, column=column, padx=padx, pady=pady)


class MessageBox():
	def __init__(self, title='Message', message='you\'re a lil bit silly mate'):
		self.messagebox = CTkMessagebox(title=title, message=message)
