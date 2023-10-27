from flask import Flask, render_template
import os
import re

import json

app = Flask(__name__)

qur = '2023q3.json'

with open(os.path.join(os.path.expanduser('~'), 'risyu', 'sv_admin', 'strodict.json'), 'r', encoding='utf-8') as f:
    strodict = json.load(f)

with open(os.path.join(os.path.expanduser('~'), 'risyu', 'sv_admin', 'weakdict.json'), 'r', encoding='utf-8') as f:
    weakdict = json.load(f)

with open(os.path.join(os.path.expanduser('~'), 'risyu', 'sv_admin', qur), 'r', encoding='utf-8') as f:
    rolelist = json.load(f)
keys_list = list(rolelist.keys())

@app.route('/')
def index():
    csvs_directory = os.path.join(os.path.expanduser('~'), 'risyu', 'csvs')
    
    with open(os.path.join(os.path.expanduser('~'), 'risyu', 'counter.txt'), 'r', encoding='utf-8') as f:
        count = f.read()
    count = int(count)
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

    with open(os.path.join(os.path.expanduser('~'), 'risyu', 'counter.txt'), 'w', encoding='utf-8') as f:
        count += 1
        f.write(str(count))

    return render_template(
        'index.html',
        theline=theline,
        asof=asof,
        rolelist=keys_list,
        weakdict=weakdict,
        strodict=strodict,
        qur=qur,
        count=count
    )

@app.route('/set')
def set():
    return render_template('set.html')

@app.route('/aff')
def aff():
    return render_template(
        'aff.html',
        rolelist=keys_list,
        qur=qur,
        rowlist=rolelist
        )

@app.route('/man')
def man():
    return render_template(
        'man.html'
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)