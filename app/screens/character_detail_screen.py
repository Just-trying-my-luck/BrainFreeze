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
		
		birth_date = tk.Label(
			self.frame,
			text=f"Born: {self.character['birth_date']}",
			font=("Helvetica", 16)
		)
		birth_date.pack(pady=10)
		
		physical_title = tk.Label(
			self.frame,
			text="PHYSICAL",
			font=("Helvetica", 20, "bold")
		)
		physical_title.pack(pady=(20, 10))
		
		physical = self.character["physical"]
		
		height = tk.Label(
			self.frame,
			text=f"Height: {physical['height']}",
			font=("Helvetica", 14)
		)
		height.pack(pady=2)
		
		build = tk.Label(
			self.frame,
			text=f"Build: {physical['build']}",
			font=("Helvetica", 14)
		)
		build.pack(pady=2)
		
		hair = tk.Label(
			self.frame,
			text=f"Hair: {physical['hair']}",
			font= ("Helvetica", 14)
		)
		hair.pack(pady=2)
		
		eyes = tk.Label(
			self.frame,
			text=f"Eyes: {physical['eyes']}",
			font=("Helvetica", 14)
		)
		eyes.pack(pady=2)
		
		features = tk.Label(
			self.frame,
			text=f"Distinguishing features: {physical['distinguishing_features']}",
			font=("Helvetica", 14)
		)
		features.pack(pady=2)
		
		back_button = tk.Button(
			self.frame,
			text="Back",
			font=("Helvetica", 14, "bold"),
			command=self.show_characters
		)
		back_button.pack(pady=20)
