import re
import os
import bs4
import csv

csvs_directory = os.path.join(os.getcwd(), 'csvs')

with open('raw.html', 'r', encoding='utf-8') as file:
    page_source = file.read()

bs = bs4.BeautifulSoup(page_source, 'html.parser')

# 指定されたtableを取得するためのコード
table = bs.find('table', {'id': 'ctl00_phContents_ucRegistrationStatus_gv'})

with open('output.tsv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    
    # ヘッダーを動的に取得して書き出す
    header_row = table.find('tr')
    headers = [header.text.strip() for header in header_row.find_all('th')]
    writer.writerow(headers)

    # 各行について情報を抽出し、TSVに書き出す
    for row in table.find_all('tr')[1:]:  # 最初の行はヘッダーなのでスキップ
        cols = row.find_all('td')
        if cols:
            data = []
            for col in cols:
                # <span>タグがあれば、そのテキストを取得
                span = col.find('span')
                if span:
                    data.append(span.text.strip().replace('\n', ' '))
                else:
                    # <td>タグ内のテキストから改行をスペースに置換
                    data.append(col.text.strip().replace('\n', ' '))
            writer.writerow(data)