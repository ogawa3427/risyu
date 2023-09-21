import os
import re
import PySimpleGUI as sg
compl=""
content = ""
header = "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望"
with open('dir.csv', "r", encoding='utf-8') as dir:
		defpath = dir.readline()

layout1 = [
[sg.Text('金沢大学教務システム - 抽選科目登録状況.htmが入っているディレクトリのフルパスを入力')], 
[sg.Text('パスを保存しておらず未入力の場合は$HOMEを見ます')], 
[sg.Checkbox("入力したパスを保存する", key="-SAVE-", default=True)], 
[sg.InputText(key='-INP-', default_text=defpath), sg.Button('実行', key='-SUBMIT-')], 
[sg.Text(compl, key='-COMPL-')], 
[sg.Text('', key='-ERROR-', size=(30, 1), text_color='red')], 
[sg.Button('(最新版を元に)表示', key='-NEXT-')]
]
window1 = sg.Window('risyu', layout1, size=(700,600))

while True:
	event, values = window1.read()
	if event=='-SUBMIT-':

#HomeOrOther
		if values['-INP-'] == "":

			if os.path.exists("dir.csv"):
				with open('dir.csv', "r", encoding='utf-8') as dir:
					path = dir.readline()
#					two = dir.readline()
#					if two:
#						print ('Error!Check your dir.csv')
				if path:
					filename = os.path.join(path, "金沢大学教務システム - 抽選科目登録状況.htm") #なしありvalid
				else:
					filename = os.path.join(os.environ["HOME"], "金沢大学教務システム - 抽選科目登録状況.htm") #なしありbrank

			else:
				filename = os.path.join(os.environ["HOME"], "金沢大学教務システム - 抽選科目登録状況.htm") #なしなし

		else: #あり
			path = values['-INP-']
			filename = os.path.join(path, "金沢大学教務システム - 抽選科目登録状況.htm")
			if values['-SAVE-'] == True:
				with open('dir.csv', 'w', encoding='utf-8') as file:
					file.write(path)
		if not os.path.exists(filename):
			window1['-ERROR-'].update('指定されたファイルが存在しません')
			continue
	elif event==sg.WIN_CLOSED:
		sta = 0
		break

	elif event=='-NEXT-':
		sta = 1
		window1.close()
		break

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


layout2 = [
[sg.Text('金沢大学教務システム - 抽選科目登録状況.htmが入っているディレクトリのフルパスを入力')], 
[sg.Checkbox("GSのみ", key="-ONLYGS-", default=True)], 
[sg.Button('月1'), sg.Button('火1'), sg.Button('水1'), sg.Button('木1'), sg.Button('金1')], 
[sg.Button('月2'), sg.Button('火2'), sg.Button('水2'), sg.Button('木2'), sg.Button('金2')], 
[sg.Button('月3'), sg.Button('火3'), sg.Button('水3'), sg.Button('木3'), sg.Button('金3')], 
[sg.Button('月4'), sg.Button('火4'), sg.Button('水4'), sg.Button('木4'), sg.Button('金4')], 
[sg.Button('月5'), sg.Button('火5'), sg.Button('水5'), sg.Button('木5'), sg.Button('金5')], 
[sg.Button('6限'), sg.Button('7限'), sg.Button('8限'), sg.Button('集中')],
[sg.Text('フリーワード'), sg.InputText(key='-WORD-'), sg.Button('検索', key='-SEARCH-')], 
[sg.Text('', key='-ERROR-', size=(30, 1), text_color='red')], 
]
window2 = sg.Window('risyu', layout2, size=(700,600))

while True:
	event, values = window2.read()
	if event == sg.WIN_CLOSED:
		break
	else:
		buttontext = event
		if buttontext == '-SEARCH-':
			buttontext = values['-WORD-']

		thelines = content

		if values['-ONLYGS-'] == True:
			thelines = '\n'.join(line for line in thelines.splitlines() if "ＧＳ" in line)
			#thelines = '\n'.join(line for line in thelines.splitlines() if "ＧＳ言語" not in line)

		thelines = '\n'.join(line for line in thelines.splitlines() if buttontext in line)




		print(thelines)