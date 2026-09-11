import tkinter as tk
from core.character_data import CHARACTERS
from screens.character_detail_screen import CharacterDetailScreen

class CharacterScreen:
		def __init__(self, parent, show_home, show_character_detail):
			self.parent = parent
			self.show_home = show_home
			self.show_character_detail = show_character_detail
			
			self.frame = tk.Frame(self.parent)
			
			title = tk.Label(
				self.frame,
				text="CHARACTER",
				font=("Helvetica", 32, "bold")
			)
			title.pack(pady=(35, 5))
		
			for character in CHARACTERS:
				button = tk.Button(
					self.frame,
					text=character["name"],
					font=("Helvetica", 16, "bold"),
					width=20,
					command=lambda c=character: self.show_character(c)
				)
				button.pack(pady=5)
			
			back_button = tk.Button(
				self.frame,
				text="BACK",
				font=("Helvetica", 14, "bold"),
				command=self.show_home
			)
			back_button.pack(pady=20)
		
		def show_character(self, character):
			self.show_character_detail(character)
