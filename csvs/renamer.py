import os
import re

def rename_files(directory):
    # ディレクトリ内の全ファイルを走査
    for filename in os.listdir(directory):
        # ファイル名が"2024"で始まるかチェック
        if filename.startswith('"2024'):
            # 新しいパターンに基づいてファイル名を変更する処理
            pattern = re.compile(r'^"(\d{4})(\d{2})(\d{2})(\d{2}):(\d{2}):(\d{2})')
            match = pattern.match(filename)
            if match:
                # 新しいファイル名の形式（YYYYMMDDhhmmss.tsv）に整形
                new_name = f"{match.group(1)}{match.group(2)}{match.group(3)}{match.group(4)}{match.group(5)}{match.group(6)}.tsv"
                original_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_name)
                # ファイル名を変更
                os.rename(original_path, new_path)
                print(f"{filename} を {new_name} にリネームしました。")
                # ここで original_path の代わりに new_path を使用
                with open(new_path, 'r', encoding='utf-8') as file:
                    input_data = file.read()
                formatted_tsv = format_to_tsv(input_data)
                # ここでは再度 new_path を使用してファイルを上書き保存
                with open(new_path, 'w', encoding='utf-8') as file:
                    file.write(formatted_tsv)

def format_to_tsv(input_data):
    # 入力データを行に分割
    lines = input_data.strip().split('\n')
    formatted_lines = []
    
    for line in lines:
        # 各行をタブで分割して列にする
        columns = line.split('\t')
        # 必要に応じてデータのクリーニングや変換を行う（ここでは省略）
        # 整形された行を追加
        formatted_lines.append('\t'.join(columns))
    
    # TSV形式の文字列に変換
    formatted_tsv = '\n'.join(formatted_lines)
    return formatted_tsv

# 使用例
directory_path = './'  # ディレクトリのパスを指定
rename_files(directory_path)
