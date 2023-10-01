
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
			subprocess.Popen(["python", "jsonwriter.py"])
			self.defpath = ''
		else:
			with open('setting.json', 'r', encoding='utf-8') as setting:
				data = json.load(setting)
				self.defpath = data['filedir']







		self.text_box.insert(0, self.defpath)




		self.save_chk.set(True) 






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





		self.radio_var.trace("w", self.update_combobox_options)



		style.configure('Large.Combobox', font=('Arial', 19))
		style.configure('Large.Combobox*Listbox', font=('Arial', 19))  # この行で選択肢の文字の大きさを変更

		if not data['newparson']:
			iki = data['iki']
			iki = re.sub('人間社会学域', '1', iki)
			iki = re.sub('理工学域', '2', iki)
			iki = re.sub('医薬保健学域', '3', iki)
			iki = re.sub('融合学域', '4', iki)
			self.radio_var.set(iki)
			self.combobox.set(data['rui'])

		self.combobox.grid(row=0,column=0, pady=20)





		nenitems = ['1年生', '2年生', '3年生', '4年生', '5年生', '6年生以上']
		self.nenbox.set(data['nen'])
		self.nenbox.grid(row=0, column=1)




	def autoinit(self):


		iki = self.radio_var.get()
		rui = self.combobox.get()
		nen = self.nenbox.get()

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
		data['nen'] = nen
		data['newparson'] = False
		with open('setting.json', 'w', encoding='utf-8') as f:
			data = json.dump(data, f, indent=4)


		self.yuul = len(self.nowyuusen)
		with open('setting.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		iki = data['iki']
		rui = data['rui']
		nen = data['nen']
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
					elif '以外' in self.nowyuusen[i]:
						gen, yuu = False, False
						iga = True
				elif nen in self.nowyuusen[i]:
					if '限定' in self.nowyuusen[i]:
						gen = True
						yuu, iga = False, False
					elif '優先' in self.nowyuusen[i]:
						yuu = True
						gen, iga = False, False
					elif '以外' in self.nowyuusen[i]:
						gen, yuu = False, False
						iga = True
				else:
					if '限定' in self.nowyuusen[i]:
						gen, yuu = False, False
						iga = True
					else:
						gen, yuu, iga = False, False, False
				initdict[self.nowyuusen[i]] = [gen, yuu, iga]
				gotoinit = json.dumps(initdict)

			with open('role.json', 'w', encoding='utf-8') as f:
				f.write(gotoinit)











		# main_frameを作成


# スクロールバーを追加


		canvas.configure(yscrollcommand=scrollbar.set)


		canvas.create_window((0, 0), window=content_frame, anchor='nw')
		content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

		with open('role.json', 'r', encoding='utf-8') as f:
			data = json.load(f)


		for i in range(1, self.yuul):
	# 各セット用のフレームを作成


			attr_name = 'kubunname' + str(i)


			block = data.get(str(self.nowyuusen[i]), [])
			vgen = block[0]
			vyuu = block[1]
			viga = block[2]

			for attr_base_name, value in [('gen', vgen), ('yuu', vyuu), ('iga', viga)]:
				attr_name = attr_base_name + str(i)

				chk_attr_name = attr_base_name + 'v' + str(i)





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

	# 厄介な書き替え
		english_class_lines = '\n'.join([line for line in content.splitlines() if '（英語クラス）' in line and line.strip()])
		english_class_lines = re.sub(r'（英語クラス）', '', english_class_lines)
		english_class_lines = '\n'.join([re.sub(r'(^[^,]*,[^,]*),', r'\1,[英]', line) for line in english_class_lines.splitlines() if line.strip()])

		non_english_class_lines = '\n'.join([line for line in content.splitlines() if '（英語クラス）' not in line and line.strip()])

		content = english_class_lines + '\n' + non_english_class_lines
		content = '\n'.join(sorted([line for line in content.splitlines() if line.strip()], key=lambda x: x.split(',')[0]))


		lines = content.split('\n')
		thelines = ''
		for line in lines:
			elements = line.split(',')

			maxer = elements[6]
			ruiseki = 0
			kyu = elements[9]
			elements[9] = int(elements[9]) - int(elements[8])
			for i in range(8,13):
				print(ruiseki)
				ruiseki = ruiseki + int(elements[i])
				if ruiseki >= int(maxer):
					elements[i] = str(elements[i]) + 'OBER'
				print(elements[i])
			elements[9] = kyu
			jele = ",".join(map(str, elements))
			thelines += jele + '\n'

	# 最後の余計な改行を取り除く
		thelines = thelines.rstrip('\n')
	






		self.buttons[(0, 0)] = btn


		self.buttons[(0, 4)] = btn




		for (row, col), btn_text in self.buttons_info.items():
	# ここで新しいボタンを作成しています。
			btn.grid(row=row, column=col, pady=5, padx=5)  # gridメソッドを使用してボタンを配置
			self.buttons[(row+1, col)] = btn




		self.buttons[(8, 0)] = btn


		self.buttons[(8, 1)] = btn


		self.buttons[(8, 2)] = btn


		self.buttons[(8, 3)] = btn




		self.onlygs_var.set(True)




		self.numo_var.set(True)


		self.ryaku_var.set(True)


		self.eng_var.set(True)


		self.dropdown_var.set(self.guns[0])





		self.buttons[(9, 5)] = btn



		self.sender = thelines


	def display_key(self, bkey):
		if bkey == 'aff':
			for widget in self.winfo_children():
				widget.destroy()
			self.whenew = 'Yes'
			self.regroll()

		elif bkey == 'sett':
			for widget in self.winfo_children():
				widget.destroy()
			self.deepsetting()

		thelines = self.sender
		atama = "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望"
		
	#検索
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

		if self.dropdown_var.get() == '全群':
			pass
		else:
			thegun = '^7' + self.dropdown_var.get() + '[A-Z]'
			print(thegun)
			theli = [line for line in thelines.split('\n') if re.search(thegun, line)]
			thelines = '\n'.join(theli)


	#教員名
		if self.tea_var.get():
			thelines = "\n".join([",".join(line.split(',')[:4] + line.split(',')[5:]) for line in thelines.strip().split("\n")])
			atama = re.sub(',教員名,' ,',' ,atama)

	#GSのみ
		if self.onlygs_var.get():
			thelines = '\n'.join(line for line in thelines.splitlines() if "ＧＳ" in line)
			thelines = '\n'.join(line for line in thelines.splitlines() if not "ＧＳ言語" in line)
			thelines = re.sub(',ＧＳ科目,', ',', thelines)
			atama = re.sub(',科目区分,' ,',' ,atama)

	#対象
		with open('role.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		if self.ryaku_var.get():
			for key, values in data.items():
				mykey = ',' + key + ','		
				if values[0]:
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


	#時間割番号
		if self.numo_var.get():
			thelines = re.sub(r'^7', '', thelines, flags=re.MULTILINE)
			thelines = re.sub(r'(?<=^.{2})[^,]+,', ',', thelines, flags=re.MULTILINE)
			atama = re.sub('時間割番号,','No.,',atama)

	#時間割名
		engdic = {}
		with open('setting.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		if data['kdoai'] == '1':
			engdic = data['kamoku_kyo']
		elif data['kdoai'] == '2':
			engdic = data['kamoku_jaku']

		if self.eng_var.get():
			for i, j in engdic.items():
				thelines = re.sub(i, j, thelines)

	#ATAMA
		if data['hanrei']:
			atama = re.sub(',対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望',',対象,適,全,優先,[１,２,３,４,５]',atama)
			atama = re.sub(',曜日時限,',', ,',atama)

		self.oklines = atama + '\n' + thelines + '\n' + atama
		self.make_table()

	def make_table(self):
		if self.outframe is not None:
			self.outframe.destroy()

		mylist = self.oklines
		ogawa = mylist.strip().split('\n')
		#ogawa.insert(0, atama)
		oklist = [line.split(',') for line in ogawa]


		rows = len(oklist)
		cols = len(oklist[0])
		frames = []
		for c in range(cols):

			frames.append(frame)
		for r in range(rows):
			for c in range(cols): 
				text = oklist[r][c]

				fg_color = "#000000"

				if "OBER" in text:
					fg_color = "#FF0000"
					text = re.sub('OBER', '', text)
				if "GRAY" in text:
					fg_color = 'LightSlateGray'
					text = re.sub('GRAY', '', text)




	def deepsetting(self):
		print('おはよう')
		with open('setting.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		




		self.kdoai.set(data['kdoai'])



	def goback(self):
		print('GOBACK')
		with open('setting.json', 'r', encoding='utf-8') as f:
			data = json.load(f)
		data['kdoai'] = self.kdoai.get()
		with open('setting.json', 'w', encoding='utf-8') as f:
			json.dump(data, f, indent=4)
		for widget in self.winfo_children():
				widget.destroy()
		self.show_buttons()

root.title('risyu')
root.geometry('900x1300')
app = Application(root=root)
root.mainloop()