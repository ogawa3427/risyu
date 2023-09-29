encoding='utf-8'
import os
import re
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Application(tk.Frame):
	def __init__(self, root):
		if not os.path.exists("setting.json"):
			initdate = {
			'filedir': '',
			'newparson': True,
			'iki': '',
			'rui': ''
	}
			gotojson = json.dumps(initdate,  indent=4)
			with open('setting.json', "w", encoding='utf-8') as set:
				set.write(gotojson) #あったら代入
			self.defpath = ''
		else:
			with open('setting.json', 'r', encoding='utf-8') as setting:
				data = json.load(setting)
				self.defpath = data['filedir']


		self.header = "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望"
		self.name = ''
		self.content = ''
		self.guns = ["全群", "1", "2", "3", "4", "5", "6"]

		super().__init__(root, width=430, height=900, borderwidth=4, relief='groove')
		self.root = root
		self.grid(sticky="nsew")

		self.buttons_info = self.generate_buttons_info()
		self.create_widgets()

		self.content = '\n'.join(sorted(self.content.split('\n'), key=lambda x: x.split(',')[0]))

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
		self.chk_vars.set(True) 
		self.chk1 = tk.Checkbutton(self, text="入力したパスを保存する", variable=self.chk_vars)
		self.chk1.grid(row=3, column=0, columnspan=2, pady=10)

		self.labelw = tk.Label(self, text="ファイルが見つかりません", fg="red")

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

	def csvmaker(self):
		self.content = ''
		self.name = ''

		inp = self.text_box.get()
		if inp:
			filepath = inp
		if not inp:
			filename = os.path.join(os.environ["HOME"], "金沢大学教務システム - 抽選科目登録状況.htm") #なしありbrank
		else: #あり
			filename = os.path.join(filepath, "金沢大学教務システム - 抽選科目登録状況.htm")
			if self.chk_vars.get():
				with open('setting.json', 'r') as file:
					data = json.load(file)
				data['filedir'] = filepath
				with open('setting.json', 'w') as file:
					json.dump(data, file, indent=4)
		if not os.path.exists(filename):
			self.labels.grid_forget()
			self.labelw.grid(row=6, column=0)

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
		self.labels.grid(row=6, column=0)
		self.labelw.grid_forget()


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
			self.content = '\n'.join(line for line in self.content.splitlines() if not "時間割番号,科目区分" in line)

		for widget in self.winfo_children():
			widget.destroy()

		self.asof = self.name + openfile
		self.asof = re.sub(r'^risyu\d{4}', '', self.asof)
		self.asof = re.sub(r'.{4}$', '', self.asof)
		patt = r"(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})"
		repl = r"\1月\2日\3:\4:\5現在"	
		self.asof = re.sub(patt, repl, self.asof)

		lines = self.content.strip().split('\n')
		sixth_items = [line.split(',')[5] for line in lines if len(line.split(',')) >= 6]
		self.nowyuusen = sorted(list(set(sixth_items)))

		self.areyounew()

	def areyounew(self):

		with open('setting.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		np = data['newparson']
		
		if not np:
			pass
		else:
			if False:
				print('OK')
				self.show_buttons()
			else:
				pass


		self.regroll()

	def update_combobox_options(self, *args):
		selected_value = self.radio_var.get()

		if selected_value == 1:
			self.combobox['values'] = ["総教文", "人文学類", "法学類", "経済学類", "学校教育学類", "地域創造学類", "国際学類"]
		elif selected_value == 2:
			self.combobox['values'] = ["総教理", "数物科学類", "物質科学類" ,"理工３学類", "機械工学類", "フロンティア工学類", "電子情報通信学類", "地球社会基盤学類", "生命理工学類"]
		elif selected_value == 3:
			self.combobox['values'] = ["医学類", "薬学類", "医薬科学類", "保健学類"]
		elif selected_value == 4:
			self.combobox['values'] = ["先導学類", "観光デザイン学類", "スマート創成科学類"]
		else:
			self.combobox['values'] = []

		self.combobox.set('')  # Clear current selection


	def regroll(self):
		with open('setting.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		rui = data['rui']
		iki = data['iki']
		iki = re.sub(r'人間社会学域', '1', iki)
		iki = re.sub(r'理工学域', '2', iki)
		iki = re.sub(r'医薬保健学域', '3', iki)
		iki = re.sub(r'融合学域', '4', iki)


		for widget in self.winfo_children():
			widget.destroy()

		self.labelr = tk.Label(self, text="あてはまる所属にチェック\n履修登録期間の初めに再度表示されることがあります\n(この画面は再度表示できます)")
		self.labelr.grid(row=0, column=0, columnspan=4, sticky="w")

		self.radio_var = tk.IntVar()
		self.radio_var.trace("w", self.update_combobox_options)
		radio1 = tk.Radiobutton(self, text="人社", variable=self.radio_var, value=1, font=("Arial", 14))
		radio2 = tk.Radiobutton(self, text="理工", variable=self.radio_var, value=2, font=("Arial", 14))
		radio3 = tk.Radiobutton(self, text="医薬保", variable=self.radio_var, value=3, font=("Arial", 14))
		radio4 = tk.Radiobutton(self, text="融合", variable=self.radio_var, value=4, font=("Arial", 14))
		radio1.grid(row=1, column=0, sticky="w")
		radio2.grid(row=1, column=1, sticky="w")
		radio3.grid(row=1, column=2, sticky="w")
		radio4.grid(row=1, column=3, sticky="w")
		

		style = ttk.Style()
		style.configure('Large.TCombobox', font=('Arial', 19))
		style.configure('Large.TCombobox*Listbox', font=('Arial', 19))  # この行で選択肢の文字の大きさを変更
		self.combobox = ttk.Combobox(self, style='Large.TCombobox', values=[] ,font=("Arial", 14))
		self.combobox.grid(row=2, column=0, columnspan=4, sticky='w')




		do_btn = tk.Button(self, text='次へ', command=self.autoinit)
		do_btn.grid(row=3, column=0, pady=10)

	def autoinit(self):
		iki = self.radio_var.get()
		rui = self.combobox.get()
		iki = re.sub(r'1', '人間社会学域', str(iki))
		iki = re.sub(r'2', '理工学域', str(iki))
		iki = re.sub(r'3', '医薬保健学域', str(iki))
		iki = re.sub(r'4', '融合学域', str(iki))
		rui = re.sub(r'学類', '', str(rui))

		with open('setting.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		data['iki'] = iki
		data['rui'] = rui
		with open('setting.json', 'w', encoding='utf-8') as f:
			data = json.dump(data, f, indent=4)


		self.yuul = len(self.nowyuusen)
		with open('setting.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		iki = data['iki']
		rui = data['rui']
		if os.path.exists("role.json"):
			initdict = {}
			for i in range(1, self.yuul):

			
				if iki in self.nowyuusen[i] or rui in self.nowyuusen[i]:
					if '限定' in self.nowyuusen[i]:
						gen = True
						yuu, iga = False, False
					elif '優先' in self.nowyuusen[i]:
						yuu = True
						gen, iga = False, False
					if '以外' in self.nowyuusen[i]:
						gen, yuu = False, False
						iga = True
				else:
					gen, yuu, iga = False, False, False
				initdict[self.nowyuusen[i]] = [gen, yuu, iga]
				gotoinit = json.dumps(initdict)

			with open('role.json', 'w', encoding='utf-8') as f:
				f.write(gotoinit)



		self.rkubun = tk.Label(self, text="区分")
		self.rkubun.grid(row=3, column=1, columnspan=1, sticky="w")
		self.rgentei = tk.Label(self, text="限定")
		self.rgentei.grid(row=3, column=4, columnspan=1, sticky="w")
		self.ryuusen = tk.Label(self, text="優先")
		self.ryuusen.grid(row=3, column=5, columnspan=1, sticky="w")
		self.ryuusen = tk.Label(self, text="以外")
		self.ryuusen.grid(row=3, column=6, columnspan=1, sticky="w")


		with open('role.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		print(data)

		for i in range(1,self.yuul):

			attr_name = 'kubunname' + str(i)
			setattr(self, attr_name, tk.Label(self, text=self.nowyuusen[i]))
			getattr(self, attr_name).grid(row=3+i, column=0, columnspan=4, sticky="w")

			block = data.get(str(self.nowyuusen[i]), [])
			vgen = block[0]
			vyuu = block[1]
			viga = block[2]


			attr_gen = 'gen' + str(i)
			setattr(self, attr_gen, tk.BooleanVar())
			getattr(self, attr_gen).set(vgen)  # BooleanVarの初期値をTrueに設定

			chk_attr_name = 'genv' + str(i)
			setattr(self, chk_attr_name, tk.Checkbutton(self, text="", variable=getattr(self, attr_gen)))
			getattr(self, chk_attr_name).grid(row=3+i, column=4, columnspan=1, sticky="w")
		
			attr_gen = 'yuu' + str(i)
			setattr(self, attr_gen, tk.BooleanVar())
			getattr(self, attr_gen).set(vyuu)  # BooleanVarの初期値をTrueに設定

			chk_attr_name = 'yuuv' + str(i)
			setattr(self, chk_attr_name, tk.Checkbutton(self, text="", variable=getattr(self, attr_gen)))
			getattr(self, chk_attr_name).grid(row=3+i, column=5, columnspan=1, sticky="w")

			attr_gen = 'iga' + str(i)
			setattr(self, attr_gen, tk.BooleanVar())
			getattr(self, attr_gen).set(viga)  # BooleanVarの初期値をTrueに設定

			chk_attr_name = 'igav' + str(i)
			setattr(self, chk_attr_name, tk.Checkbutton(self, text="", variable=getattr(self, attr_gen)))
			getattr(self, chk_attr_name).grid(row=3+i, column=6, columnspan=1, sticky="w")



		back_btn = tk.Button(self, text='完了', command=self.backtothelist)
		back_btn.grid(row=i+4, column=0, pady=10)


	def backtothelist(self):
		for widget in self.winfo_children():
			widget.destroy()
		self.show_buttons()


	def show_buttons(self):
		self.headers_list = self.header.split(',')



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
		self.onlygs_var.set(True)
		self.onlygs_chk = tk.Checkbutton(self, text="GSのみ", variable=self.onlygs_var)  # こちらも変数名を変更
		self.onlygs_chk.grid(row=1, column=5, columnspan=1, pady=1)

		self.tea_var = tk.BooleanVar()
		self.tea_chk = tk.Checkbutton(self, text="教員名を省略", variable=self.tea_var)  # こちらも変数名を変更
		self.tea_chk.grid(row=2, column=5, columnspan=1, pady=1)

		self.numo_var = tk.BooleanVar()
		self.numo_var.set(True)
		self.numo_chk = tk.Checkbutton(self, text="時間割番号を省略", variable=self.numo_var)  # こちらも変数名を変更
		self.numo_chk.grid(row=3, column=5, columnspan=1, pady=1)

		self.ryaku_var = tk.BooleanVar()
		self.ryaku_var.set(True)
		self.ryaku_chk = tk.Checkbutton(self, text="優先/限定を簡略化", variable=self.ryaku_var)  # こちらも変数名を変更
		self.ryaku_chk.grid(row=4, column=5, columnspan=1, pady=1)

		self.dropdown_var = tk.StringVar(self)
		self.dropdown_var.set(self.guns[0])
		self.dropdown_menu = tk.OptionMenu(self, self.dropdown_var, *self.guns)
		self.dropdown_menu.grid(row=8, column=4, pady=1, padx=1, columnspan=1)

		self.ser_box = tk.Entry(self, width=30)
		self.ser_box.grid(row=9, column=0, columnspan=5, pady=10)

		btn = tk.Button(self, text="フリーワード検索", command=lambda k="search": self.display_key(k))
		btn.grid(row=9, column=5, pady=1, padx=1)
		self.buttons[(9, 5)] = btn







	def display_key(self, key):
		thelines = self.content
		if key == 'aff':
			self.regroll()

		#トグル系スクリーニング/書き換え
		print('こんにちは')

		if self.dropdown_var.get() == '全群':
			pass
		else:
			thegun = '^7' + self.dropdown_var.get() + '[A-Z].*?\n$'
			thelines = re.sub(thegun, '', thelines)
			print(thegun)

		if self.onlygs_var.get():
			print('OK')
			thelines = '\n'.join(line for line in thelines.splitlines() if "ＧＳ" in line)
			thelines = '\n'.join(line for line in thelines.splitlines() if not "ＧＳ言語" in line)

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
				if key == '6限' or key == '7限' or key == '8限':
					key = re.sub(r'限', '', key)
					key = '(月|火|水|木|金)' + key
				thelines = '\n'.join(line for line in thelines.splitlines() if re.search(key, line))
		print(key)

	


root = tk.Tk()
root.title('risyu')
root.geometry('720x900')
app = Application(root=root)
root.mainloop()