import tkinter as tk
from screens.home_screen import HomeScreen
from screens.character_screen import CharacterScreen
from screens.character_detail_screen import CharacterDetailScreen

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650

class BrainFreezeApp:

	def __init__(self, root):
		self.root = root

		root.title("Brain Freeze")
		root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
		root.minsize(800, 550)

		self.home_screen = HomeScreen(
			self.root,
			self.show_character
		)
		
		self.character_screen = CharacterScreen(
			self.root,
			self.show_home,
			self.show_character_detail
		)
		
		self.home_screen.frame.pack()
	
	def show_character(self):
		self.home_screen.frame.pack_forget()
		
		if hasattr(self, "character_detail_screen"):
			self.character_detail_screen.frame.pack_forget()
			
		self.character_screen.frame.pack()
		
	def show_home(self):
		self.character_screen.frame.pack_forget()
		self.home_screen.frame.pack()
		
	def show_character_detail(self, character):
		self.character_screen.frame.pack_forget()
		self.character_detail_screen = CharacterDetailScreen(
			self.root,
			character,
			self.show_character
		)
		self.character_detail_screen.frame.pack()
	
def main():
	root = tk.Tk()
	app = BrainFreezeApp(root)
	root.mainloop()
		
if __name__ == "__main__":
	main()
