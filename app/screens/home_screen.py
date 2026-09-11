import tkinter as tk

class HomeScreen:
	def __init__(self, parent, show_character):
		self.parent = parent
		self.show_character = show_character
		
		self.frame = tk.Frame(self.parent)
		
		title=tk.Label(
			self.parent,
			text="BRAIN FREEZE",
			font=("Helvetica", 32, "bold")
		)
		title.pack(pady=(35, 5))
			
		subtitle = tk.Label(
			self.frame,
			text= "Promise Series Directory",
			font=("Helvetica", 16)
		)
		subtitle.pack(pady=(0, 30))
		
		character_button = tk.Button(
			self.frame,
			text="CHARACTER",
			font=("Helvetica", 14, "bold"),
			command=self.show_character
		)
		character_button.pack(pady=20)
