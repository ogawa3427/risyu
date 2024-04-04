import re
import os
import csv

# ディレクトリのパスを指定
directory_path = './'

# 指定したディレクトリ内のtsvファイルのリストを取得し、名前で昇順にソート
tsv_files = sorted([file for file in os.listdir(directory_path) if file.endswith('.tsv') and '2024' in file])

pattern = re.compile(r'^"[^"]*"$')

new_lines = []
dns = {}
#tsv_files = [ "20240403230701.tsv" ]
for tsv_file in tsv_files:
    #print(tsv_file)
    with open(tsv_file, 'r', encoding='utf-8') as file:
        input_data = file.read()
    # 入力データを行に分割
    lines = input_data.strip().split('\n')
    lines = [pattern.sub('', line) for line in lines]
    lines = lines[2:]
    for line in lines:
        line = line.split('\\t')
        if not all(cell == '"' for cell in line):
            #print(line)

            try:
                if line[0] not in dns:
                    dns[line[0]] = [line[1], line[2], line[3], line[4], line[5]]
                
                new_lines.append([tsv_file.replace('.tsv', ''), line[0], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13]])

            except:
                print(line)
                print(tsv_file)



#print(lines)
with open('output.tsv', 'w', encoding='utf-8') as file:
    for line in new_lines:
        file.write('\t'.join(line) + '\n')

print('output.tsv を作成しました。')

with open('output_dns.tsv', 'w', encoding='utf-8') as file:
    for key in dns:
        file.write(key + '\t' + '\t'.join(dns[key]) + '\n')

print('output_dns.tsv を作成しました。')