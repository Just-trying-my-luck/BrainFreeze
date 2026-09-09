import tkinter as tk

def main():
	root = tk.Tk()
	root.title("Brain Freeze")
	root.geometry("1000x650")

	title = tk.Label(
		root,
		text="BRAIN FREEZE",
		font=("Helvetica", 32, "bold")
	)
	title.pack(pady=40)

	subtitle = tk.Label(
		root,
		text="Promise Series Directory",
		font=("Helvetica", 18)
	)
	subtitle.pack()

	status = tk.Label(
		root,
		text="SYSTEM READY",
		font=("Helvetica", 14)
	)
	status.pack(pady=40)

	root.mainloop()

if __name__ == "__main__":
	main()
