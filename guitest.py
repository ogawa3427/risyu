encoding='utf-8'
# -*- coding: utf-8 -*-
import sys
import codecs
import os
import re
import PySimpleGUI as sg
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

layout1 = [
[sg.Text('金沢大学教務システム - 抽選科目登録状況.htmが')], 
[sg.Text('入っているディレクトリのフルパスを入力')], 
[sg.Text('パスを保存しておらず未入力の場合は$HOMEを見ます')], 
[sg.Checkbox("入力したパスを保存する", key="-SAVE-", default=True), sg.Checkbox("新しいパスに更新", key="-IGN-", default=False)], 
[sg.InputText(key='-INP-', default_text=defpath), sg.Button('実行', key='-SUBMIT-')], 
[sg.Text(compl, key='-COMPL-')], 
[sg.Text('', key='-ERROR-', size=(30, 1), text_color='red')], 
[sg.Button('(最新版を元に)表示', key='-NEXT-')]
]
window1 = sg.Window('risyu', layout1, size=(500, 300), keep_on_top=True)

while True:
	event, values = window1.read()

	if event=='-SUBMIT-':
		if values['-IGN-']:
			defpath = values['-INP-']
		if not values['-INP-']:
			filename = os.path.join(os.environ["HOME"], "金沢大学教務システム - 抽選科目登録状況.htm") #なしありbrank
		else: #あり
			filename = os.path.join(defpath, "金沢大学教務システム - 抽選科目登録状況.htm")
			if values['-SAVE-']:
				with open('dir.csv', 'w', encoding='utf-8') as file:
					file.write(defpath)
		if not os.path.exists(filename):
			window1['-ERROR-'].update('指定されたファイルが存在しません')
			window1['-COMPL-'].update('')
			continue

		with open(filename, 'r', encoding='utf-8') as f:
			line = f.readline()
			mode = 0
			#turn = 1
			while line:
				if "ctl00_phContents_ucRegistrationStatus_lb" in line:
					name = line
				if '                        </tbody></table>' in line:
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



	elif event==sg.WIN_CLOSED:
		sta = 0
		break

	elif event=='-NEXT-':
		sta = 1
		if not content:
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
		window1.close()
		break


asof = name + openfile
asof = re.sub(r'^risyu\d{4}', '', asof)
asof = re.sub(r'.{4}$', '', asof)
patt = r"(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})"
repl = r"\1月\2日\3:\4:\5現在"
asof = re.sub(patt, repl, asof)


guns = ["全群", "1", "2", "3", "4", "5", "6"]

layout2 = [
[sg.Text(asof)], 
[sg.Checkbox("GSのみ", key="-ONLYGS-", default=True)], 
[sg.Button('月1'), sg.Button('火1'), sg.Button('水1'), sg.Button('木1'), sg.Button('金1')], 
[sg.Button('月2'), sg.Button('火2'), sg.Button('水2'), sg.Button('木2'), sg.Button('金2')], 
[sg.Button('月3'), sg.Button('火3'), sg.Button('水3'), sg.Button('木3'), sg.Button('金3')], 
[sg.Button('月4'), sg.Button('火4'), sg.Button('水4'), sg.Button('木4'), sg.Button('金4')], 
[sg.Button('月5'), sg.Button('火5'), sg.Button('水5'), sg.Button('木5'), sg.Button('金5')], 
[sg.Button('6限'), sg.Button('7限'), sg.Button('8限'), sg.Button('集中'), sg.Combo(guns, key='-GUN-', size=(4,1), default_value='全群')],
[sg.InputText(key='-WORD-', size=(20,1)), sg.Button('フリーワード検索', key='-SEARCH-', size=(17,1))], 
[sg.Checkbox("担当教員表示", key="-TEA-", default=True), sg.Checkbox("時間割番号を省略", key="-RYA-", default=True)],
[sg.Text('', key='-ERROR-', size=(30, 1), text_color='red')], 
[sg.Text('',key='-RES-',font=('Arial',20))] 
]
window2 = sg.Window('risyu', layout2, size=(550,900), keep_on_top=True)

while True:

	if sta == 0:
		break
	thelines = content
	event, values = window2.read()

	if event == sg.WIN_CLOSED:
		break
	
	else:
		buttontext = event
		if buttontext == '-SEARCH-':
			buttontext = values['-WORD-']
		thelines = '\n'.join(line for line in thelines.splitlines() if buttontext in line)

		if values['-ONLYGS-'] == True:
			thelines = '\n'.join(line for line in thelines.splitlines() if "ＧＳ" in line)
			thelines = '\n'.join(line for line in thelines.splitlines() if not "ＧＳ言語" in line)
			thelines = re.sub(r',ＧＳ科目', '', thelines)

		if re.match(r"^\d", values['-GUN-']):
			gunkey = "^7" + values['-GUN-'] + "[A-F]"
			thelines = '\n'.join(line for line in thelines.splitlines() if re.search(gunkey, line))

		if not values['-TEA-']:
			thelines = "\n".join([",".join(re.split(',', line)[:3] + re.split(',', line)[5:]) for line in thelines.strip().split("\n")])

		if values['-RYA-']:
			thelines = re.sub(r'^7', '', thelines, flags=re.MULTILINE)
			thelines = re.sub(r'(?<=^.{2})[^,]+,', ',', thelines, flags=re.MULTILINE)

#きんにくん
			#thelines = re.sub(r',{2,}', ',', thelines)
		#print(thelines)
		window2['-RES-'].update(thelines)