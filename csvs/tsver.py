import csv
import os

directory = './'
for file_path in os.listdir(directory):
    if file_path.startswith('2024'):
        # ファイルを読み込み、内容を一時的に保存
        with open(file_path, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file, delimiter='\t')
            rows = list(reader)

        # 修正したデータをファイルに書き込む
        with open(file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(rows)

        print(f'{file_path} の内容を修正しました。')