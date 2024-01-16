import customtkinter as ctk
import CTkMessagebox


# TODO convert these classes to inherit the ctk.class stuff and then mess with the constructor to fix any errors
# TODO convert all ctk widgets into classes for future use
class App(ctk.CTk):
	def __init__(self, width, height, title, icon=None):
		super().__init__()
		self.geometry(f'{width}x{height}')
		self.resizable(True, True)
		self.title(title)
		self.buttons = []
		self.labels = []
		self.entries = []
		self.frames = []
		ctk.set_appearance_mode('System')
		ctk.set_default_color_theme('dark-blue')
		if icon is not None:
			self.iconbitmap(icon)


class Frame(ctk.CTkFrame):
	def __init__(self, master, width, height, xpos, ypos, **kwargs):
		super().__init__(master=master, width=width, height=height, **kwargs)
		self.place(x=xpos, y=ypos)
		self.buttons = []
		self.labels = []
		self.entries = []

class Button(ctk.CTkButton):
	def __init__(self, master, button_text='CTkButton', xpos=0, ypos=0, command=None, **kwargs):
		super().__init__(master=master, command=command, text=button_text, **kwargs)
		self.place(x=xpos, y=ypos)


class Label():
	def __init__(self, window, xpos=0, ypos=0, text='', font_type='Georgia', font_size=24,
				 fg_color='transparent', text_color='blue'):
		self.label = ctk.CTkLabel(window, text=text, font=(font_type, font_size))
		self.label.place(x=xpos, y=ypos)
		self.text = text
		self.font = (font_type, font_size)
		self.fg_color = fg_color
		self.text_color = text_color

	def update_label(self, name):
		self.label.configure(text=self.text, text_color=self.text_color, font=self.font)


class EntryBox():
	def __init__(self, window, placeholder_text='Enter text', xpos=0, ypos=0):
		self.entry = ctk.CTkEntry(window, placeholder_text=placeholder_text)
		self.entry.place(x=xpos, y=ypos)


class MessageBox():
	def __init__(self, title='Message', message='you\'re a lil bit silly mate'):
		self.messagebox = CTkMessagebox.CTkMessagebox(title=title, message=message)
