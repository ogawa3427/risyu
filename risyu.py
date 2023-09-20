import os
import re

#dir,csvありますかチェック
if os.path.exists("dir.csv"):
    print ('aru')
    with open('dir.csv', "r", encoding='utf-8') as dir:
        path = dir.readline()
        two = dir.readline()
        if two:
            print ('Error!Check your dir.csv')
        filename = os.path.join(path, "金沢大学教務システム - 抽選科目登録状況.htm")

else:
    print ('nai')
    filename = os.path.join(os.environ["HOME"], "金沢大学教務システム - 抽選科目登録状況.htm")

print (filename)

with open(filename, 'r', encoding='utf-8') as f:
    line = f.readline()
    mode = 0
    while line:
        if '						</tbody></table>' in line:
            mode = 2
        if mode == 1:
            print (line, end="")
        if '						<table' in line:
            mode = 1
 

"""
# Extract name
name_pattern = r'ctl00_phContents_ucRegistrationStatus_lblDate.*?>([^<]+)<'
name_match = re.search(name_pattern, content)
if name_match:
    name = re.sub(r'[ :/]', '', name_match.group(1))

# Extract table content
table_content = re.search(r'<table.*?>(.*?)<\/tbody><\/table>', content, re.DOTALL).group(1)
table_content = re.sub(r'\r', '', table_content)
table_content = re.sub(r'\n', '', table_content)

# Convert table content to CSV format
rows = re.split(r'<\/tr><tr style="background-color:[^>]+>', table_content)
csv_rows = []
for row in rows:
    cells = re.findall(r'<td>([^<]+)<\/td>', row)
    csv_rows.append(','.join(cells))

csv_content = '\n'.join(csv_rows)

# Write the CSV content to file
header = "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望"
with open(f"risyu{name}.csv", 'w', encoding='utf-8') as f:
    f.write(header + '\n' + csv_content)

name
"""