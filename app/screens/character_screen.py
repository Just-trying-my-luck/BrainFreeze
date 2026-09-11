import tkinter as tk

class CharacterScreen:
		def __init__(self, parent, show_home):
			self.parent = parent
			self.show_home= show_home
			
			self.frame = tk.Frame(self.parent)
			
			title = tk.Label(
				self.frame,
				text="CHARACTER",
				font=("Helvetica", 32, "bold")
			)
			title.pack(pady=(35, 5))
			
			back_button = tk.Button(
				self.frame,
				text="BACK",
				font=("Helvetica", 14, "bold"),
				command=self.show_home
			)
			back_button.pack(pady=20)
