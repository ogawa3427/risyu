import sys

# コマンドライン引数からファイル名を取得
filename = sys.argv[1]

with open(filename, 'r') as file:
    for line in file:
        # カンマの数が3つ以上（つまり、カンマで区切られたフィールドが4つ以上）あるかチェック
        if line.count(',') >= 3:
            print(line, end='')
