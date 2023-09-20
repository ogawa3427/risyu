import os
import re

header = "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望"
#dir,csvありますかチェック
if os.path.exists("dir.csv"):
    with open('dir.csv', "r", encoding='utf-8') as dir:
        path = dir.readline()
        two = dir.readline()
        if two:
            print ('Error!Check your dir.csv')
        filename = os.path.join(path, "金沢大学教務システム - 抽選科目登録状況.htm")
else:
    filename = os.path.join(os.environ["HOME"], "金沢大学教務システム - 抽選科目登録状況.htm")

with open(filename, 'r', encoding='utf-8') as f:
    line = f.readline()
    mode = 0
    #turn = 1
    content = ""
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
    content = header + content

name = re.sub(r'<.*?>', '', name)
name = re.sub(r'\t', '', name)
name = re.sub(r'[ :\/]', '', name)
name = re.sub(r'\n', '', name)
name = "risyu" + name
name = name + ".csv"

with open(name, 'w', encoding='utf-8') as file:
    file.write(content)
