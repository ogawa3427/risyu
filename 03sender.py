from flask import Flask, jsonify
import os
import csv
import json
import re

app = Flask(__name__)
app.json.ensure_ascii = False

csvs_directory = os.path.join(os.path.expanduser('~'), 'risyu', 'csvs')

@app.route('/api', methods=['GET'])
def get_example():
    # 'csvs'ディレクトリ内のファイルとディレクトリのリストを取得
    ls = os.listdir(csvs_directory)
    ls = [ls for ls in ls if re.search("risyu", ls)]
    ls = [ls for ls in ls if re.search("csv", ls)]

    numlist = [re.findall(r'\d+', fname)[0] for fname in ls if re.findall(r'\d+', fname)]
    openfile = max(numlist)
    openfile = re.sub(r'^', 'risyu', openfile)
    openfile = re.sub(r'$', '.csv', openfile)
    # 'csvs'ディレクトリ内のファイルを開く
    with open(os.path.join(csvs_directory, openfile), 'r', encoding='utf-8') as f:
        theline = ''.join(line for line in f if True)
        theline = re.sub('\n','eskape', theline)

    asof = max(numlist)
    patt = r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})"
    repl = r"\1年\2月\3日\4:\5:\6現在"
    asof = re.sub(patt, repl, asof)


#lines = rowdata.splitlines()
#reader = csv.reader(lines)
#jsondata = json.dumps(list(reader), ensure_ascii=False)
    data = {
        'header' : "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望",
        'csv': theline,
        'asof': asof
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
