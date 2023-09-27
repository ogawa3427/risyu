import tkinter



class Application(tkinter.Frame):
	def __init__(self,root):
		super().__init__(root, width=420, height=320, borderwidth=4, relief='groove')
		self.root = root
		self.pack()
		self.pack_propagate(0)
		self.create_widgets()

	def create_widgets(self):
		quit_btn = tkinter.Button(self)
		quit_btn['text']='閉じる'
		quit_btn['command']=self.root.destroy
		quit_btn.pack(side='bottom')

		self.text_box = tkinter.Entry(self)
		self.text_box['width'] = 10
		self.text_box.pack()

		submit_btn = tkinter.Button(self)
		submit_btn['text'] = '実行'
		submit_btn['command'] = self.input_handler
		submit_btn.pack()

		self.messeage = tkinter.Message(self)
		self.messeage.pack()

	def input_handler(self):
		text = self.text_box.get()
		self.messeage['text'] = text + '!'


root = tkinter.Tk()
root.title('risyu')
root.geometry('400x600')
app = Application(root=root)
root.mainloop()