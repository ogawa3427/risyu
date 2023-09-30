import tkinter as tk

def create_table(root, rows, cols):
	for r in range(rows):
		for c in range(cols):
			frame = tk.Frame(
				root,
				relief="solid",
				bd=1
			)
			frame.grid(row=r, column=c, sticky='nsew')
			label = tk.Label(frame, text=f"R{r+1}C{c+1}")
			label.pack(fill='both', expand=True)
	for r in range(rows):
		root.grid_rowconfigure(r, weight=1)
	for c in range(cols):
		root.grid_columnconfigure(c, weight=1)

root = tk.Tk()
root.title("Table using Label & Frame")
create_table(root, 13, 10)
root.mainloop()
