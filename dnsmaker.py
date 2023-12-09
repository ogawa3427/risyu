import csv
import json

# CSVファイルのパス
csv_file_path = 'dns.csv'

# JSONファイルのパス
json_file_path = 'dns.json'

# CSVファイルを読み込んで、一対一の辞書を作成する
data = {}
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        if len(row) >= 2:
            key = row[0]
            value = row[1]
            data[key] = value

# JSON形式でファイルに書き出す（ASCIIエスケープなし）
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
