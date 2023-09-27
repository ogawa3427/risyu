encoding='utf-8'
# -*- coding: utf-8 -*-
import io
import sys
import codecs
import os
import re
import pandas as pd
import PySimpleGUI as sg
import tkinter as tk
from tkinter import messagebox

sg.set_options(font=("MS Gothic", 14))
sg.theme("DarkBlue")
compl=""
content = ""
header = "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望"
defpath=''
name = ""
openfile = ""

if os.path.exists("dir.csv"):
	with open('dir.csv', "r", encoding='utf-8') as dir:
		defpath = dir.readline() #あったら代入





class Application(tk.Frame):
	def __init__(self, root):
		super().__init__(root, width=400, height=800, borderwidth=4, relief='groove')
		self.root = root
		self.grid(sticky="nsew")
		self.create_widgets()

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
		self.text_box.grid(row=5, column=0, columnspan=2, pady=10)

		quit_btn = tk.Button(self, text='実行', command=self.csvmaker)
		quit_btn.grid(row=5, column=2, columnspan=1, pady=10)


	def input_handler(self):
		text = self.text_box.get()
		self.messeage['text'] = text + '!'

	def go_next(self):
		sta = 1
		pwd='.'
		ls = os.listdir(pwd)
		newls = [ls for ls in ls if re.search("risyu", ls)]
		newestls = [newls for newls in newls if re.search("csv", newls)]

		numlist = [re.findall(r'\d+', fname)[0] for fname in newestls if re.findall(r'\d+', fname)]
		openfile = max(numlist)
		openfile = re.sub(r'^', 'risyu', openfile)
		openfile = re.sub(r'$', '.csv', openfile)
		with open(openfile,'r', encoding='utf-8') as ofile:
			line = ofile.readline()
			content = ""
			while line:
				content += line
				line = ofile.readline()
			content = re.sub(r'^時間割番号,.*+$\n', '', content)

		
		for widget in self.winfo_children():
			widget.destroy()			#print(content)
		print(content)

	def csvmaker(self):
		inp = text_box.get()
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
			window1['-ERROR-'].update('指定されたファイルが存在しません')
			window1['-COMPL-'].update('')

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
					content += line
				if 'th align' in line:
					mode = 1
				line = f.readline()
			#print (turn)
			#turn += 1
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
		contents = header + content

		name = re.sub(r'<.*?>', '', name)
		name = re.sub(r'\t', '', name)
		name = re.sub(r'[ :\/]', '', name)
		name = re.sub(r'\n', '', name)
		name = "risyu" + name
		name = name + ".csv"

		with open(name, 'w', encoding='utf-8') as file:
			file.write(contents)
		compl = "保存しました" + name
		window1['-COMPL-'].update(compl)
		window1['-ERROR-'].update('')



root = tk.Tk()
root.title('risyu')
root.geometry('450x250')
app = Application(root=root)
root.mainloop()




while True:
	event, values = window1.read()

	if event=='-SUBMIT-':




	elif event==sg.WIN_CLOSED:
		sta = 0
		break


asof = name + openfile
asof = re.sub(r'^risyu\d{4}', '', asof)
asof = re.sub(r'.{4}$', '', asof)
patt = r"(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})"
repl = r"\1月\2日\3:\4:\5現在"
asof = re.sub(patt, repl, asof)


guns = ["全群", "1", "2", "3", "4", "5", "6"]


layout2 = [
[sg.Text(asof), sg.Button('高度な設定', key='-SET-', size=(17,1)), sg.Button('所属設定', key='-AFF-', size=(17,1))], 
[sg.Button('月1'), sg.Button('火1'), sg.Button('水1'), sg.Button('木1'), sg.Button('金1'), sg.Checkbox("GSのみ", key="-ONLYGS-", default=True)], 
[sg.Button('月2'), sg.Button('火2'), sg.Button('水2'), sg.Button('木2'), sg.Button('金2'), sg.Checkbox("担当教員を省略", key="-TEA-", default=False)], 
[sg.Button('月3'), sg.Button('火3'), sg.Button('水3'), sg.Button('木3'), sg.Button('金3'), sg.Checkbox("時間割番号を省略", key="-RYA-", default=True)], 
[sg.Button('月4'), sg.Button('火4'), sg.Button('水4'), sg.Button('木4'), sg.Button('金4'), sg.Checkbox("優先/限定を簡略化", key="-RYA-", default=True)], 
[sg.Button('月5'), sg.Button('火5'), sg.Button('水5'), sg.Button('木5'), sg.Button('金5')], 
[sg.Button('6限'), sg.Button('7限'), sg.Button('8限'), sg.Button('集中'), sg.Combo(guns, key='-GUN-', size=(4,1), default_value='全群')],
[sg.InputText(key='-WORD-', size=(20,1)), sg.Button('フリーワード検索', key='-SEARCH-', size=(17,1))], 
[sg.Text('', key='-ERROR-', size=(30, 1), text_color='red')], 
[sg.Text('',key='-RES0-',font=('Meiryo',10)),
sg.Text('',key='-RES1-',font=('Meiryo',10)),
sg.Text('',key='-RES2-',font=('Meiryo',10)),
sg.Text('',key='-RES3-',font=('Meiryo',10)),
sg.Text('',key='-RES4-',font=('Meiryo',10)),
sg.Text('',key='-RES5-',font=('Meiryo',10)),
sg.Text('',key='-RES6-',font=('Meiryo',10)),
sg.Text('',key='-RES7-',font=('Meiryo',10)),
sg.Text('',key='-RES8-',font=('Meiryo',10)),
sg.Text('',key='-RES9-',font=('Meiryo',10)),
sg.Text('',key='-RES10-',font=('Meiryo',10)),
sg.Text('',key='-RES11-',font=('Meiryo',10)),
sg.Text('',key='-RES12-',font=('Meiryo',10)),
sg.Text('',key='-RES13-',font=('Meiryo',10)),
] 
]
window2 = sg.Window('risyu', layout2, size=(550,900), keep_on_top=True)


#厄介な書き換え
english_class_lines = '\n'.join([line for line in content.split('\n') if '（英語クラス）' in line])

english_class_lines = re.sub(r'（英語クラス）', '', english_class_lines)
english_class_lines = '\n'.join([re.sub(r'(^[^,]*,[^,]*),', r'\1,[英]', line) for line in english_class_lines.split('\n')])

non_english_class_lines = '\n'.join([line for line in content.split('\n') if '（英語クラス）' not in line])

content = non_english_class_lines + '\n' + english_class_lines

#並べ替え
content = '\n'.join(sorted(content.split('\n'), key=lambda x: x.split(',')[0]))


#main loop
while True:
	event, values = window2.read()
	thelines = content
	if sta == 0:
		break

	elif event == sg.WIN_CLOSED:
		break
	
	else:
		#トグル系スクリーニング/書き換え
		if values['-ONLYGS-'] == True:
			thelines = '\n'.join(line for line in thelines.splitlines() if "ＧＳ" in line)
			thelines = '\n'.join(line for line in thelines.splitlines() if not "ＧＳ言語" in line)
			thelines = re.sub(r',ＧＳ科目', '', thelines)

		if values['-TEA-']:
			thelines = "\n".join([",".join(re.split(',', line)[:3] + re.split(',', line)[5:]) for line in thelines.strip().split("\n")])

		if values['-RYA-']:
			thelines = re.sub(r'^7', '', thelines, flags=re.MULTILINE)
			thelines = re.sub(r'(?<=^.{2})[^,]+,', ',', thelines, flags=re.MULTILINE)

		if re.match(r"^\d", values['-GUN-']):
			if values['-RYA-']:
				gunkey = "^" + values['-GUN-'] + "[A-F]"
			else:
				gunkey = "^7" + values['-GUN-'] + "[A-F]"
			thelines = '\n'.join(line for line in thelines.splitlines() if re.search(gunkey, line))

		print(thelines)

		buttontext = event
		if buttontext == '-SEARCH-':
			buttontext = values['-WORD-']
		thelines = '\n'.join(line for line in thelines.splitlines() if buttontext in line)


#格納&表示
		split_lines = [line.split(',') for line in thelines.split('\n')]
		num_columns = len(split_lines[0])

		res = {}
		updated_columns = set()  # このセットで更新された列番号をトラッキングします

		for n in range(num_columns):
			res[n] = [row[n] for row in split_lines]

			if res[n]:
				updated_columns.add(n)
			for n, column_data in res.items():
				print(f'res[{n}] = {column_data}')

			data_str = '\n'.join(column_data)
			window2[f'-RES{n}-'].update(data_str)

		#ガベコレ的な
		for i in range(14):
			if i not in updated_columns:
				window2[f'-RES{i}-'].update('')