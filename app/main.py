import tkinter as tk
from screens.home_screen import HomeScreen
from screens.character_screen import CharacterScreen
from screens.character_detail_screen import CharacterDetailScreen

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650
LOADING_TIME_MS = 1500


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


def show_loading_screen(root):
    """Display the startup screen, then launch the main application."""
    loading_frame = tk.Frame(root, bg="#111827")
    loading_frame.pack(fill="both", expand=True)

    tk.Label(
        loading_frame,
        text="BRAIN FREEZE INITIALIZING...",
        font=("Helvetica", 36, "bold"),
        fg="#F9FAFB",
        bg="#111827"
    ).pack(expand=True)

    # Give Tk time to paint the loading screen before building the app.
    root.after(LOADING_TIME_MS, lambda: start_application(root, loading_frame))


def start_application(root, loading_frame):
    loading_frame.destroy()
    BrainFreezeApp(root)


def main():
    root = tk.Tk()
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.minsize(800, 550)
    show_loading_screen(root)
    root.mainloop()


if __name__ == "__main__":
    main()
