import tkinter as tk

class CharacterDetailScreen:
	def __init__(self, parent, character, show_characters):
		self.parent = parent
		self.character = character
		self.show_characters = show_characters
		
		self.frame = tk.Frame(self.parent)
		
		title = tk.Label(
			self.frame,
			text=self.character["name"],
			font=("Helvetica", 32, "bold")
		)
		title.pack(pady=(35, 5))
		
		role = tk.Label(
			self.frame,
			text=self.character["role"],
			font=("Helvetica", 16)
		)
		role.pack(pady=10)
		
		back_button = tk.Button(
			self.frame,
			text="Back",
			font=("Helvetica", 14, "bold"),
			command=self.show_characters
		)
		back_button.pack(pady=20)
