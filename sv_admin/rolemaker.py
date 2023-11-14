import json

# ファイルを開いて各行をリストに読み込む
with open('rowroles', 'r', encoding='utf-8') as f:
    rowroles = [line.strip() for line in f]

# 改行文字が除去されたリストを表示

#重複を削除
rowroles = list(set(rowroles))

#print(rowroles)

with open('2023q3.json', 'r', encoding='utf-8') as f:
    rolelist = json.load(f)

dictkeys = set(rolelist.keys())

rowroles = list(set(rowroles) - dictkeys)

print(rowroles)