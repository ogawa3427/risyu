import re
import os
csvs_directory = os.path.join(os.getcwd(), 'csvs')

import json
import csv
import time

#source = "金沢大学教務システム - 抽選科目登録状況.htm"
source = 'page_source.html'

toggle = 0
scptname = '02csv_maker'

while True:
	try:
		with open(source, 'r', encoding='utf-8') as f:
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
		#header = "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望"
		#contents = header + '\n' + content
		contents = content
		#こんなことしかできない自分のことが大嫌いだ
		contents = contents.replace("月2,火2", "月2，火2")

		name = re.sub(r'<.*?>', '', name)
		name = re.sub(r'\t', '', name)
		name = re.sub(r'[ :\/]', '', name)
		name = re.sub(r'\n', '', name)
		name = "risyu" + name
		name = name + ".csv"
		
		path = os.path.join(csvs_directory, name)
		with open(path, 'w', encoding='utf-8') as file:
			file.write(contents)

		print('CSV_made_sucsessfuly')
		print(path)

		with open('deadoralive.json', 'r', encoding='utf-8') as f:
			deadoralive = json.load(f)
		
		deadoralive[scptname][scptname + str(toggle)] = int(time.time()/1)

		diff01 = abs(deadoralive[scptname][scptname + '0'] - deadoralive[scptname][scptname + '1'])
		deadoralive[scptname][scptname + '_diff'] = diff01

		with open('deadoralive.json', 'w', encoding='utf-8') as f:
			json.dump(deadoralive, f, indent=4)

		toggle = 1 - toggle

		current_second = time.localtime().tm_sec
		sleeptime = 60 - current_second
		time.sleep(sleeptime)    
	except:

		print('CSV_error')

