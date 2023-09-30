encoding='utf-8'
import os
import re
import json
import tkinter as tk
from tkinter import ttk



class Application(tk.Frame):
	def __init__(self, root):
		import pretty_errors
		pretty_errors.activate()
		name = ''
		content = ''
		self.guns = ["全群", "1", "2", "3", "4", "5", "6"]
		self.buttons = {} 
		self.outframe = None
		self.whenew = ''

		super().__init__(root, width=1000, height=2000, borderwidth=4, relief='groove')
		self.root = root
		self.pack()

		self.buttons_info = self.generate_buttons_info()
		self.create_widgets()
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
		if not os.path.exists("setting.json"): #初回起動かどうか
			initdate = {
			'filedir': '',
			'newparson': True,
			'iki': '',
			'rui': ''
	}
			with open('setting.json', "w", encoding='utf-8') as f:
				json.dump(initdate, f)
			self.defpath = ''
		else:
			with open('setting.json', 'r', encoding='utf-8') as setting:
				data = json.load(setting)
				self.defpath = data['filedir']


		label1 = tk.Label(self, text="金沢大学教務システム - 抽選科目登録状況.htmが")
		label1.pack(anchor=tk.N)
		label2 = tk.Label(self, text="入っているディレクトリのフルパスを入力")
		label2.pack()
		label3 = tk.Label(self, text="パスを保存しておらず未入力の場合は$HOMEを見ます")
		label3.pack()

		start1 = tk.Frame(self, width=100, height=200)
		start1.pack()
		self.text_box = tk.Entry(start1, width=40)
		self.text_box.insert(0, self.defpath)
		self.text_box.pack(side=tk.LEFT)
		quit_btn = tk.Button(start1, text='実行', command=self.csvmaker)
		quit_btn.pack(side=tk.LEFT)

		start2 = tk.Frame(self, width=100, height=200)
		start2.pack(side=tk.RIGHT, pady=8)
		self.save_chk = tk.BooleanVar()
		self.save_chk.set(True) 
		self.chk1 = tk.Checkbutton(start2, text="入力したパスを保存する", variable=self.save_chk)
		self.chk1.pack(side=tk.LEFT, anchor=tk.W, padx=(0,50))
		quit_btn = tk.Button(start2, text='(最新版を)表示', command=self.go_next, width=10)
		quit_btn.pack(side=tk.RIGHT, padx=(10,0))

		start3 = tk.Frame(self, width=50, height=50)
		start3.pack()
		self.labelw = tk.Label(self, text="ファイルが見つかりません", fg="red")
		self.labels = tk.Label(self, text="保存しました[ファイル名]")


	def csvmaker(self):
		if self.text_box.get(): #空ならHOME
			filepath = os.path.join(self.text_box.get(), "金沢大学教務システム - 抽選科目登録状況.htm")
		else:
			filepath = os.path.join(os.environ["HOME"], "金沢大学教務システム - 抽選科目登録状況.htm") #なしありbrank

		if self.save_chk.get():
			with open('setting.json', 'r') as f:
				data = json.load(f)
			data['filedir'] = self.text_box.get()
			with open('setting.json', 'w') as f:
				json.dump(data, f, indent=4)

		if not os.path.exists(filepath):
			self.labels.pack_forget()
			self.labelw.pack(anchor=tk.CENTER, side=tk.TOP)

		with open(filepath, 'r', encoding='utf-8') as f:
			line = f.readline()
			mode = 0
			content=''
			name = ''
			while line:
				if "ctl00_phContents_ucRegistrationStatus_lb" in line:
					name = line
				if '						</tbody></table>' in line:
					mode = 2
				if mode == 1:
					if "</tr><tr" in line:
						line = "eskape"
					content += line
				if 'th align' in line:
					mode = 1
				line = f.readline()

		content = content.replace(" ", "")
		content = content.replace("\t", "")
		content = content.replace("\n", "")
		content = content.replace("</span>", "")
		content = re.sub(r'<span.*?>', '', content)
		content = re.sub(r'<td.*?>', '<td>', content)
		content = content.replace("</td><td>", ",")
		content = content.replace("<td>", "")
		content = content.replace("</td>", "")
		content = content.replace("&amp;", "&")
		content = re.sub(r'<\/tr>.*', '', content)

		content = re.sub(r'^\n', '', content)
		content = content.replace("eskape", "\n")
		header = "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望"
		contents = header + '\n' + content

		name = re.sub(r'<.*?>', '', name)
		name = re.sub(r'\t', '', name)
		name = re.sub(r'[ :\/]', '', name)
		name = re.sub(r'\n', '', name)
		name = "risyu" + name
		name = name + ".csv"
		
		with open(name, 'w', encoding='utf-8') as file:
			file.write(contents)

		name = '保存しました' + name
		self.labels.config(text=name)
		self.labels.pack(anchor=tk.CENTER, side=tk.TOP)
		self.labelw.pack_forget()


	def go_next(self):
		ls = os.listdir('.')
		ls = [ls for ls in ls if re.search("risyu", ls)]
		ls = [ls for ls in ls if re.search("csv", ls)]

		numlist = [re.findall(r'\d+', fname)[0] for fname in ls if re.findall(r'\d+', fname)]
		openfile = max(numlist)
		openfile = re.sub(r'^', 'risyu', openfile)
		openfile = re.sub(r'$', '.csv', openfile)
		content = ''
		with open(openfile, 'r', encoding='utf-8') as f:
			content = ''.join(line for line in f if "時間割番号,科目区分" not in line)
		for widget in self.winfo_children():
			widget.destroy()
		print(content)

		self.asof = openfile
		self.asof = re.sub(r'^risyu\d{4}', '', self.asof)
		self.asof = re.sub(r'.{4}$', '', self.asof)
		patt = r"(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})"
		repl = r"\1月\2日\3:\4:\5現在"	
		self.asof = re.sub(patt, repl, self.asof)

		lines = content.strip().split('\n')
		sixth_items = [line.split(',')[5] for line in lines if len(line.split(',')) >= 6]
		self.nowyuusen = sorted(list(set(sixth_items)))

		self.content = content
		self.areyounew()

	def areyounew(self):
		with open('setting.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		if data['newparson']:
			self.regroll()
		else:
			self.show_buttons()


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

		for widget in self.winfo_children():
			widget.destroy()

		self.labelr = tk.Label(self, text="あてはまる所属にチェック\n履修登録期間の初めに再度表示されることがあります\n(この画面は再度表示できます)")
		self.labelr.pack()

		radio_f = tk.Frame(self)
		radio_f.pack(pady=10)

		self.radio_var = tk.IntVar()
		self.radio_var.trace("w", self.update_combobox_options)
		radio1 = tk.Radiobutton(radio_f, text="人社", variable=self.radio_var, value=1, font=("Arial", 14))
		radio2 = tk.Radiobutton(radio_f, text="理工", variable=self.radio_var, value=2, font=("Arial", 14))
		radio3 = tk.Radiobutton(radio_f, text="医薬保", variable=self.radio_var, value=3, font=("Arial", 14))
		radio4 = tk.Radiobutton(radio_f, text="融合", variable=self.radio_var, value=4, font=("Arial", 14))

		style = ttk.Style()
		style.configure('Large.TCombobox', font=('Arial', 19))
		style.configure('Large.TCombobox*Listbox', font=('Arial', 19))  # この行で選択肢の文字の大きさを変更
		self.combobox = ttk.Combobox(self, style='Large.TCombobox', values=[] ,font=("Arial", 14))


		if not data['newparson']:
			iki = data['iki']
			iki = re.sub('人間社会学域', '1', iki)
			iki = re.sub('理工学域', '2', iki)
			iki = re.sub('医薬保健学域', '3', iki)
			iki = re.sub('融合学域', '4', iki)
			self.radio_var.set(iki)
			self.combobox.set(data['rui'])

		self.combobox.pack(anchor=tk.CENTER, pady=20)
		radio1.pack(anchor = tk.W, side=tk.LEFT, padx=5)
		radio2.pack(side = tk.LEFT, padx=5)
		radio3.pack(side = tk.LEFT, padx=5)
		radio4.pack(side = tk.LEFT, padx=5)


		do_btn = tk.Button(self, text='次へ', command=self.autoinit)
		do_btn.pack(anchor=tk.CENTER, fill=tk.X)

	def autoinit(self):


		iki = self.radio_var.get()
		rui = self.combobox.get()

		iki = re.sub(r'1', '人間社会学域', str(iki))
		iki = re.sub(r'2', '理工学域', str(iki))
		iki = re.sub(r'3', '医薬保健学域', str(iki))
		iki = re.sub(r'4', '融合学域', str(iki))
		rui = re.sub(r'学類', '', str(rui))

		print(iki)
		print(rui)


		with open('setting.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		data['iki'] = iki
		data['rui'] = rui
		data['newparson'] = False
		with open('setting.json', 'w', encoding='utf-8') as f:
			data = json.dump(data, f, indent=4)


		self.yuul = len(self.nowyuusen)
		with open('setting.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		iki = data['iki']
		rui = data['rui']
		if not os.path.exists("role.json"):
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


		outer_frame = tk.Frame(self, width=400, height=400)
		outer_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

		self.rkubun = tk.Label(outer_frame, text="区分")
		self.rkubun.pack(anchor=tk.W, side=tk.LEFT)

		rframe = tk.Frame(outer_frame, width=700, height=650)
		rframe.pack(padx=10, side=tk.RIGHT)

		self.ryuusen = tk.Label(rframe, text="以外 ", font=('Arial, 16'))
		self.ryuusen.pack(side=tk.LEFT)
		self.ryuusen2 = tk.Label(rframe, text="優先 ", font=('Arial, 16'))
		self.ryuusen2.pack(side=tk.LEFT)
		self.rgentei = tk.Label(rframe, text="限定 ", font=('Arial, 16'))
		self.rgentei.pack(anchor=tk.NE, side=tk.LEFT, fill=tk.X, expand=True)
		# main_frameを作成
		main_frame = tk.Frame(self, width=700, height=650)
		main_frame.pack(fill=tk.BOTH, expand=True)

# スクロールバーを追加
		canvas = tk.Canvas(main_frame, width=800, height=690)
		canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		scrollbar = tk.Scrollbar(main_frame, command=canvas.yview)
		canvas.configure(yscrollcommand=scrollbar.set)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		content_frame = tk.Frame(canvas, width=400, height=700)
		canvas.create_window((0, 0), window=content_frame, anchor='nw')
		content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

		with open('role.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		#print(data)

		for i in range(1, self.yuul):
	# 各セット用のフレームを作成
			set_frame = tk.Frame(content_frame, borderwidth=1, relief="solid")
			set_frame.pack(fill=tk.X, padx=5, pady=5, expand=True)

			attr_name = 'kubunname' + str(i)
			setattr(self, attr_name, tk.Label(set_frame, text=self.nowyuusen[i]))
			getattr(self, attr_name).pack(side=tk.LEFT)

			block = data.get(str(self.nowyuusen[i]), [])
			vgen = block[0]
			vyuu = block[1]
			viga = block[2]

			for attr_base_name, value in [('gen', vgen), ('yuu', vyuu), ('iga', viga)]:
				attr_name = attr_base_name + str(i)
				setattr(self, attr_name, tk.BooleanVar(value=value))

				chk_attr_name = attr_base_name + 'v' + str(i)
				setattr(self, chk_attr_name, tk.Checkbutton(set_frame, text="", variable=getattr(self, attr_name)))
				getattr(self, chk_attr_name).pack(side=tk.RIGHT, padx=5)

		back_btn = tk.Button(self, text='完了', command=self.backtothelist)
		back_btn.pack()


	def backtothelist(self):


		with open('role.json', 'r', encoding='utf-8') as f:
			data = json.load(f)

		with open('role.json', 'w', encoding='utf-8') as f:
			for i in range(1, self.yuul):
				key = str(self.nowyuusen[i])
				vgen = getattr(self, 'gen' + str(i)).get()
				vyuu = getattr(self, 'yuu' + str(i)).get()
				viga = getattr(self, 'iga' + str(i)).get()
				data[key] = [vgen, vyuu, viga]
		
			json.dump(data, f, ensure_ascii=False, indent=4)

		for widget in self.winfo_children():
			widget.destroy()
		self.show_buttons()


	def show_buttons(self):
		content = self.content
		#厄介な書き替え
		#print(content)
		english_class_lines = '\n'.join([line for line in content.split('\n') if '（英語クラス）' in line])
		english_class_lines = re.sub(r'（英語クラス）', '', english_class_lines)
		english_class_lines = '\n'.join([re.sub(r'(^[^,]*,[^,]*),', r'\1,[英]', line) for line in english_class_lines.split('\n')])
		non_english_class_lines = '\n'.join([line for line in content.split('\n') if '（英語クラス）' not in line])
		content = english_class_lines + non_english_class_lines
		content = '\n'.join(sorted(content.split('\n'), key=lambda x: x.split(',')[0]))

		lines = content.split('\n')
		thelines = ''
		for line in lines:
			elements = line.split(',')

			maxer = elements[6]
			ruiseki = 0
			elements[9] = int(elements[9]) - int(elements[8])
			for i in range(8,13):
				ruiseki = ruiseki + int(elements[i])
				if ruiseki >= int(maxer):
					elements[i] = str(elements[i]) + 'OBER'
			jele = ",".join(map(str, elements))
			thelines = thelines + jele + '\n'

				
		contf = tk.Frame(self, width=700, height=650)

		frame1 = tk.Frame(contf, width=700, height=650)
		frame1.pack(padx=20,pady=20, side=tk.TOP)

		self.labelasof = tk.Label(frame1, text=self.asof)
		self.labelasof.pack(side=tk.LEFT, padx=20)

		btn = tk.Button(frame1, text="高度な設定", command=lambda k="sett": self.display_key(k))
		btn.pack(side=tk.LEFT, padx=20)
		self.buttons[(0, 0)] = btn

		btn = tk.Button(frame1, text="所属設定", command=lambda k="aff": self.display_key(k))
		btn.pack(side=tk.LEFT, padx=20)
		self.buttons[(0, 4)] = btn

		lframe = tk.Frame(contf, width=700, height=700)

		frame2 = tk.Frame(lframe, width=700, height=650)
		frame2.pack(padx=10, side=tk.TOP)

		for (row, col), btn_text in self.buttons_info.items():
	# ここで新しいボタンを作成しています。
			btn = tk.Button(frame2, text=btn_text, command=lambda k=btn_text: self.display_key(k))  # parent引数をframe2に変更
			btn.grid(row=row, column=col, pady=5, padx=5)  # gridメソッドを使用してボタンを配置
			self.buttons[(row+1, col)] = btn

		frame3 = tk.Frame(lframe, width=700, height=650)
		frame3.pack(padx=1,pady=1, side=tk.TOP)

		btn = tk.Button(frame3, text="6限", command=lambda k="6限": self.display_key(k))
		btn.pack(side=tk.LEFT, padx=5)
		self.buttons[(8, 0)] = btn

		btn = tk.Button(frame3, text="7限", command=lambda k="7限": self.display_key(k))
		btn.pack(side=tk.LEFT, padx=5)
		self.buttons[(8, 1)] = btn

		btn = tk.Button(frame3, text="8限", command=lambda k="8限": self.display_key(k))
		btn.pack(side=tk.LEFT, padx=5)
		self.buttons[(8, 2)] = btn

		btn = tk.Button(frame3, text="集中", command=lambda k="集中": self.display_key(k))
		btn.pack(side=tk.LEFT, padx=5)
		self.buttons[(8, 3)] = btn

		lframe.pack(side=tk.LEFT)



		frame4 = tk.Frame(contf, width=700, height=650)
		frame4.pack(padx=1,pady=1, side=tk.RIGHT, after=frame1)

		self.onlygs_var = tk.BooleanVar()
		self.onlygs_var.set(True)
		self.onlygs_chk = tk.Checkbutton(frame4, text="GSのみ", variable=self.onlygs_var)  # こちらも変数名を変更
		self.onlygs_chk.pack(anchor=tk.W)

		self.tea_var = tk.BooleanVar()
		self.tea_chk = tk.Checkbutton(frame4, text="教員名を省略", variable=self.tea_var)  # こちらも変数名を変更
		self.tea_chk.pack(anchor=tk.W)

		self.numo_var = tk.BooleanVar()
		self.numo_var.set(True)
		self.numo_chk = tk.Checkbutton(frame4, text="時間割番号を省略", variable=self.numo_var)  # こちらも変数名を変更
		self.numo_chk.pack(anchor=tk.W)

		self.ryaku_var = tk.BooleanVar()
		self.ryaku_var.set(True)
		self.ryaku_chk = tk.Checkbutton(frame4, text="優先/限定を簡略化", variable=self.ryaku_var)  # こちらも変数名を変更
		self.ryaku_chk.pack(anchor=tk.W)

		self.eng_var = tk.BooleanVar()
		self.eng_var.set(True)
		self.eng_chk = tk.Checkbutton(frame4, text="科目名を省略", variable=self.eng_var)  # こちらも変数名を変更
		self.eng_chk.pack(anchor=tk.W)

		self.dropdown_var = tk.StringVar(self)
		self.dropdown_var.set(self.guns[0])
		self.dropdown_menu = tk.OptionMenu(frame4, self.dropdown_var, *self.guns)
		self.dropdown_menu.pack(anchor=tk.W)

		self.ser_box = tk.Entry(frame4, width=30)
		self.ser_box.pack(anchor=tk.W)

		btn = tk.Button(frame4, text="フリーワード検索", command=lambda k="search": self.display_key(k))
		btn.pack(anchor=tk.W)
		self.buttons[(9, 5)] = btn

		contf.pack(padx=20,pady=20, side=tk.TOP)

		self.sender = thelines


	def display_key(self, bkey):
		thelines = self.sender
		if bkey == 'aff':
			for widget in self.winfo_children():
				widget.destroy()
			self.whenew = 'Yes'
			self.regroll()

		with open('role.json', 'r', encoding='utf-8') as f:
			data = json.load(f)


		if self.ryaku_var.get():
			for key, values in data.items():
				mykey = ',' + key + ','		
				if values[0]:
					print('oho')
					thelines = re.sub(mykey, ',優,', thelines)
				elif values[1]:
					thelines = re.sub(mykey, ',限,', thelines)
				elif values[2]:
					thelines = re.sub(mykey, ',外,', thelines)
				else:
					thelines = re.sub(mykey, ', ,', thelines)

		lines = thelines.strip().split('\n')
		for i, line in enumerate(lines):
	# ',外,'が含まれる行を見つける
			if ',外,' in line:
		# その行の各要素の末尾に"GRAY"を追加
				lines[i] = ','.join([item + 'GRAY' for item in line.split(',')])
		thelines = '\n'.join(lines)

		if self.dropdown_var.get() == '全群':
			pass
		else:
			thegun = '^7' + self.dropdown_var.get() + '[A-Z].*?\n$'
			thelines = re.sub(thegun, '', thelines)
			#print(thegun)

		if self.tea_var.get():
			thelines = "\n".join([",".join(re.split(',', line)[:4] + re.split(',', line)[5:]) for line in thelines.strip().split("\n")])
		#print(thelines)

		if self.onlygs_var.get():
			thelines = '\n'.join(line for line in thelines.splitlines() if "ＧＳ" in line)
			thelines = '\n'.join(line for line in thelines.splitlines() if not "ＧＳ言語" in line)
			thelines = re.sub(',ＧＳ科目', '', thelines)


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
			if bkey == 'search':
				pass
			else:
				if bkey == '6限' or bkey == '7限' or bkey == '8限':
					bkey = re.sub(r'限', '', bkey)
					bkey = '(月|火|水|木|金)' + bkey
				thelines = '\n'.join(line for line in thelines.splitlines() if re.search(bkey, line))

		engdic = {
		'グローバル時代の': 'ｸﾞﾛｰﾊﾞﾙ時代の',
		'エクササイズ&スポーツ': 'E&S',
		'インテグレーテッド': 'インテグ',
		'論理学から': '',
		'異文化間コミュニケーション': '異コミュ',
		'グローバル': 'ｸﾞﾛｰﾊﾞﾙ',
		'ケーススタディ': 'ｹｰｽｽﾀﾃﾞｨ',
		'PHILLIPPSJEREMYDAVID': 'PHILLIPPS',
		'GRUENEBERGPATRICK': 'GRUENEBERG',
		'アプローチ': 'ｱﾌﾟﾛｰﾁ'
		}

		if self.eng_var.get():
			for i, j in engdic.items():
				thelines = re.sub(i, j, thelines)

		self.oklines = thelines
		self.make_table()

	def make_table(self):
		atama = "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望"

		print(atama)
		if self.onlygs_var:
			atama = re.sub('科目区分,', '', atama)

		if self.tea_var:
			atama = re.sub('教員名,','',atama)

		atama = re.sub('対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望','対象,適,全,優先,[１,２,３,４,５]',atama)
		atama = re.sub('時間割番号','No.',atama)
		atama = re.sub('曜日時限', '', atama)
		if self.outframe is not None:
			self.outframe.destroy()
		#print(self.oklines)
		mylist = self.oklines
		ogawa = mylist.strip().split('\n')
		ogawa.insert(0, atama)
		oklist = [line.split(',') for line in ogawa]

		rows = len(oklist)
		cols = len(oklist[0])
		self.outframe = tk.Frame(self, width=700, height=700)
		frames = []
		for c in range(cols):
			frame = tk.Frame(self.outframe, width=700, height=700)
			frame.pack(side=tk.LEFT, padx=5, pady=5)
			frames.append(frame)
		for r in range(rows):
			for c in range(cols): 
				text = oklist[r][c]

				if "OBER" in text:
					fg_color = "red"
					text = re.sub('OBER', '', text)
				if "GRAY" in text:
					fg_color = 'LightSlateGray'
					text = re.sub('GRAY', '', text)
				else:
					fg_color = "black"

				label = tk.Label(frames[c], text=text, anchor=tk.W, fg=fg_color)
				label.pack(fill='both', expand=True)
		self.outframe.pack()
root = tk.Tk()
root.title('risyu')
root.geometry('900x1300')
app = Application(root=root)
root.mainloop()