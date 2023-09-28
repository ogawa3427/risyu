encoding='utf-8'
# -*- coding: utf-8 -*-
import io
import sys
import codecs
import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Application(tk.Frame):
	def __init__(self, root):
		if os.path.exists("dir.csv"):
			with open('dir.csv', "r", encoding='utf-8') as dir:
				self.defpath = dir.readline() #あったら代入

		self.header = "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望"
		self.name = ''
		self.content = ''
		self.guns = ["全群", "1", "2", "3", "4", "5", "6"]


		super().__init__(root, width=400, height=800, borderwidth=4, relief='groove')
		self.root = root
		self.grid(sticky="nsew")

		self.buttons_info = self.generate_buttons_info()
		self.create_widgets()

		self.content = '\n'.join(sorted(self.content.split('\n'), key=lambda x: x.split(',')[0]))

		self.tree = None

	def generate_buttons_info(self):
		days = ["月", "火", "水", "木", "金"]
		info = {}

		for row in range(1, 6):  # 1から5までのループ
			for col, day in enumerate(days):
				key = (row, col)
				value = f"{day}{row}"
				info[key] = value
		return info



	def create_widgets(self):
		self.label1 = tk.Label(self, text="金沢大学教務システム - 抽選科目登録状況.htmが")
		self.label1.grid(row=0, column=0, columnspan=3, sticky="w")

		self.label2 = tk.Label(self, text="入っているディレクトリのフルパスを入力")
		self.label2.grid(row=1, column=0, columnspan=3, sticky="w")

		self.label3 = tk.Label(self, text="パスを保存しておらず未入力の場合は$HOMEを見ます")
		self.label3.grid(row=2, column=0, columnspan=3, sticky="w")

		self.chk_vars = tk.BooleanVar()
		self.chk1 = tk.Checkbutton(self, text="入力したパスを保存する", variable=self.chk_vars)
		self.chk1.grid(row=3, column=0, columnspan=2, pady=10)

		self.chk_varr = tk.BooleanVar()
		self.chk2 = tk.Checkbutton(self, text="新しいパスに更新", variable=self.chk_varr)
		self.chk2.grid(row=3, column=2, columnspan=1, pady=10)

		self.labelw = tk.Label(self, text="ファイルが見つかりません")
		self.labelw.grid(row=0, column=0)
		self.labelw.grid_forget()

		self.labels = tk.Label(self, text="保存しました[ファイル名]")
		self.labels.grid(row=0, column=0)
		self.labels.grid_forget()

		quit_btn = tk.Button(self, text='最新版を表示', command=self.go_next, width=10)
		quit_btn.grid(row=4, column=0, columnspan=1, pady=10)

		self.text_box = tk.Entry(self, width=30)
		self.text_box.insert(0, self.defpath)
		self.text_box.grid(row=5, column=0, columnspan=2, pady=10)

		quit_btn = tk.Button(self, text='実行', command=self.csvmaker)
		quit_btn.grid(row=5, column=2, columnspan=1, pady=10)

		self.buttons = {}  # すべてのボタンをこの辞書に保存

		for (row, col), btn_text in self.buttons_info.items():
			btn = tk.Button(self, text=btn_text, command=lambda k=btn_text: self.display_key(k))
			#btn.grid(row=row, column=col, pady=10, padx=10)
			self.buttons[(row, col)] = btn  # ボタンを辞書に追加



	def go_next(self):
		pwd = '.'
		ls = os.listdir(pwd)
		newls = [ls for ls in ls if re.search("risyu", ls)]
		newestls = [newls for newls in newls if re.search("csv", newls)]

		numlist = [re.findall(r'\d+', fname)[0] for fname in newestls if re.findall(r'\d+', fname)]
		openfile = max(numlist)
		openfile = re.sub(r'^', 'risyu', openfile)
		openfile = re.sub(r'$', '.csv', openfile)
		with open(openfile,'r', encoding='utf-8') as ofile:
			line = ofile.readline()
			while line:
				self.content += line
				line = ofile.readline()
			self.content = re.sub(r'^時間割番号,.*+$\n', '', self.content)

		
		for widget in self.winfo_children():
			widget.destroy()

		self.asof = self.name + openfile
		self.asof = re.sub(r'^risyu\d{4}', '', self.asof)
		self.asof = re.sub(r'.{4}$', '', self.asof)
		patt = r"(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})"
		repl = r"\1月\2日\3:\4:\5現在"	
		self.asof = re.sub(patt, repl, self.asof)

		self.show_buttons()

	def csvmaker(self):
		inp = self.text_box.get()
		if inp:
			defpath = inp
		if not inp:
			filename = os.path.join(os.environ["HOME"], "金沢大学教務システム - 抽選科目登録状況.htm") #なしありbrank
		else: #あり
			filename = os.path.join(defpath, "金沢大学教務システム - 抽選科目登録状況.htm")
			if self.chk_vars.get():
				with open('dir.csv', 'w', encoding='utf-8') as file:
					file.write(defpath)
		if not os.path.exists(filename):
			self.labels.config(text='')
			self.labelw.config(text='ファイルが見つかりません')

		with open(filename, 'r', encoding='utf-8') as f:
			line = f.readline()
			mode = 0
			#turn = 1
			while line:
				if "ctl00_phContents_ucRegistrationStatus_lb" in line:
					name = line
				if '						</tbody></table>' in line:
					mode = 2
				if mode == 1:
					if "</tr><tr" in line:
						line = "eskape"
					self.content += line
				if 'th align' in line:
					mode = 1
				line = f.readline()

		self.content = self.content.replace(" ", "")
		self.content = self.content.replace("\t", "")
		self.content = self.content.replace("\n", "")
		self.content = self.content.replace("</span>", "")
		self.content = re.sub(r'<span.*?>', '', self.content)
		self.content = re.sub(r'<td.*?>', '<td>', self.content)
		self.content = self.content.replace("</td><td>", ",")
		self.content = self.content.replace("<td>", "")
		self.content = self.content.replace("</td>", "")
		self.content = self.content.replace("&amp;", "&")
		self.content = re.sub(r'<\/tr>.*', '', self.content)

		self.content = re.sub(r'^\n', '', self.content)
		self.content = self.content.replace("eskape", "\n")
		self.contents = self.header + self.content

		self.name = re.sub(r'<.*?>', '', self.name)
		self.name = re.sub(r'\t', '', self.name)
		self.name = re.sub(r'[ :\/]', '', self.name)
		self.name = re.sub(r'\n', '', self.name)
		self.name = "risyu" + self.name
		self.name = self.name + ".csv"

		with open(self.name, 'w', encoding='utf-8') as file:
			file.write(self.contents)

		self.name = '保存しました' + self.name
		self.labels.config(text=self.name)
		self.labelw.config(text='')

	def show_buttons(self):
		btn = tk.Button(self, text="高度な設定", command=lambda k="sett": self.display_key(k))
		btn.grid(row=0, column=0, pady=1, padx=1, columnspan=3)
		self.buttons[(0, 0)] = btn

		btn = tk.Button(self, text="所属設定", command=lambda k="aff": self.display_key(k))
		btn.grid(row=0, column=3, pady=1, padx=1, columnspan=3)
		self.buttons[(0, 4)] = btn

		self.labelasof = tk.Label(self, text=self.asof)
		self.labelasof.grid(row=1, column=0, columnspan=5)

		for (row, col), btn_text in self.buttons_info.items():
			# ここで新しいボタンを作成しています。
			btn = tk.Button(self, text=btn_text, command=lambda k=btn_text: self.display_key(k))
			btn.grid(row=row+1, column=col, pady=1, padx=1)
			self.buttons[(row+1, col)] = btn

		btn = tk.Button(self, text="6限", command=lambda k="6限": self.display_key(k))
		btn.grid(row=8, column=0, pady=1, padx=1)
		self.buttons[(8, 0)] = btn

		btn = tk.Button(self, text="7限", command=lambda k="7限": self.display_key(k))
		btn.grid(row=8, column=1, pady=1, padx=1)
		self.buttons[(8, 1)] = btn

		btn = tk.Button(self, text="8限", command=lambda k="8限": self.display_key(k))
		btn.grid(row=8, column=2, pady=1, padx=1)
		self.buttons[(8, 2)] = btn

		btn = tk.Button(self, text="集中", command=lambda k="集中": self.display_key(k))
		btn.grid(row=8, column=3, pady=1, padx=1)
		self.buttons[(8, 3)] = btn

		self.onlygs_var = tk.BooleanVar()
		self.onlygs_chk = tk.Checkbutton(self, text="GSのみ", variable=self.onlygs_var)  # こちらも変数名を変更
		self.onlygs_chk.grid(row=1, column=5, columnspan=1, pady=1)

		self.tea_var = tk.BooleanVar()
		self.tea_chk = tk.Checkbutton(self, text="教員名を省略", variable=self.tea_var)  # こちらも変数名を変更
		self.tea_chk.grid(row=2, column=5, columnspan=1, pady=1)

		self.numo_var = tk.BooleanVar()
		self.numo_chk = tk.Checkbutton(self, text="時間割番号を省略", variable=self.numo_var)  # こちらも変数名を変更
		self.numo_chk.grid(row=3, column=5, columnspan=1, pady=1)

		self.ryaku_var = tk.BooleanVar()
		self.ryaku_chk = tk.Checkbutton(self, text="優先/限定を簡略化", variable=self.ryaku_var)  # こちらも変数名を変更
		self.ryaku_chk.grid(row=4, column=5, columnspan=1, pady=1)

		self.dropdown_var = tk.StringVar(self)
		self.dropdown_var.set(self.guns[0])
		self.dropdown_menu = tk.OptionMenu(self, self.dropdown_var, *self.guns)
		self.dropdown_menu.grid(row=8, column=4, pady=1, padx=1, columnspan=2)

		self.ser_box = tk.Entry(self, width=30)
		self.ser_box.grid(row=9, column=0, columnspan=5, pady=10)

		btn = tk.Button(self, text="フリーワード検索", command=lambda k="search": self.display_key(k))
		btn.grid(row=9, column=5, pady=1, padx=1)
		self.buttons[(9, 5)] = btn


		table_frame = ttk.Frame(self)
		table_frame.grid(row=10, column=0, columnspan=12, pady=10, padx=10, sticky='nsew')
		self.table = ttk.Treeview(table_frame, columns=('A', 'B', 'C'))
		self.table.pack(fill=tk.BOTH, expand=True)

		if not hasattr(self, 'tree') or not self.tree:
			self.tree = ttk.Treeview(self, columns=("Column1", "Column2", "Column3"))
			self.tree.grid(row=10, column=0, columnspan=10)






	def display_key(self, key):
		thelines = self.content

		#トグル系スクリーニング/書き換え
		print('こんにちは')

		if self.dropdown_var.get() == '全群':
			pass
		else:
			thegun = '^7' + self.dropdown_var.get() + '[A-Z].*?\n$'
			thelines = re.sub(thegun, '', thelines)
			print(thegun)

		if self.tea_var.get():
			thelines = "\n".join([",".join(re.split(',', line)[:4] + re.split(',', line)[5:]) for line in thelines.strip().split("\n")])

		if self.onlygs_var.get():
			print('OK')
			thelines = '\n'.join(line for line in thelines.splitlines() if "ＧＳ" in line)
			thelines = '\n'.join(line for line in thelines.splitlines() if not "ＧＳ言語" in line)
			thelines = re.sub(r',ＧＳ科目', '', thelines)

		if self.numo_var.get():
			thelines = re.sub(r'^7', '', thelines, flags=re.MULTILINE)
			thelines = re.sub(r'(?<=^.{2})[^,]+,', ',', thelines, flags=re.MULTILINE)

		if re.match(r"^\d", self.dropdown_var.get()):
			if self.numo_var.get():
				gunkey = "^" +  self.dropdown_var.get() + "[A-F]"
			else:
				gunkey = "^7" +  self.dropdown_var.get() + "[A-F]"
			thelines = '\n'.join(line for line in thelines.splitlines() if re.search(gunkey, line))


		
		buttontext = self.ser_box.get()
		if buttontext:
			thelines = '\n'.join(line for line in thelines.splitlines() if buttontext in line)
		else:
			if key == 'search':
				pass
			else:
				thelines = '\n'.join(line for line in thelines.splitlines() if key in line)
		print(key)

		
		#print(thelines)

		# 既存のエントリをクリア
		for item in self.tree.get_children():
			self.tree.delete(item)

	# データの挿入
		lines_list = [line.split(",") for line in thelines.split("\n") if line]
		for item in lines_list:
			self.tree.insert("", "end", values=(item[0], item[1], item[2]))

	# 再描画のトリガー
		self.tree.update_idletasks()



root = tk.Tk()
root.title('risyu')
root.geometry('450x900')
app = Application(root=root)
root.mainloop()



