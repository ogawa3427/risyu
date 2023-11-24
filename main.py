from flask import Flask, render_template, redirect
import os
import re
import json
import csv
import time
from flask import jsonify

app = Flask(__name__)

qur = '2023q4.json'

app.json.ensure_ascii = False

csvs_directory = os.path.join(os.path.expanduser('~'), 'risyu', 'csvs')

count = 0

with open(os.path.join(os.path.expanduser('~'), 'risyu', 'sv_admin', 'strodict.json'), 'r', encoding='utf-8') as f:
    strodict = json.load(f)

with open(os.path.join(os.path.expanduser('~'), 'risyu', 'sv_admin', 'weakdict.json'), 'r', encoding='utf-8') as f:
    weakdict = json.load(f)

with open(os.path.join(os.path.expanduser('~'), 'risyu', 'sv_admin', qur), 'r', encoding='utf-8') as f:
    rolelist = json.load(f)
keys_list = list(rolelist.keys())

with open('dns.json', 'r', encoding='utf-8') as f:
    dns = json.load(f)
    #print(dns)

with open(os.path.join(os.path.expanduser('~'), 'risyu', 'sv_admin', 'depander.json'), 'r', encoding='utf-8') as f:
    parent_depander = json.load(f)
if str(os.environ.get('RISYU_ENV')):
    depander = parent_depander['dev']
    print('dev')
else:
    depander = parent_depander['prod']
    print('prod')

@app.route('/')
def index():
    global count
    with open(os.path.join(os.path.expanduser('~'), 'risyu', 'counter.txt'), 'w', encoding='utf-8') as f:
        count += 1
        f.write(str(count))

    return render_template(
        'index.html',
        rolelist=keys_list,
        weakdict=weakdict,
        strodict=strodict,
        qur=qur,
        count=count,
        linka = depander['linka'],
        fetcher = depander['fetcher'],
        mode = 'hose'
    )

@app.route('/img/<string:id>')
def img(id):
    img_path = f'/imgs/{id}.png'
    print(img_path)

    fullname = dns[id]
    return render_template(
        'img.html',
        id=id,
        img_path=img_path,
        fullname=fullname
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

@app.route('/api', methods=['GET'])
def get_example():
    with open('recieved.json', 'r', encoding='utf-8') as f:
        recieved = json.load(f)
        recieved['header'] = "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,登録数,残数"
    res = jsonify(recieved)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

@app.route('/deadoralive')
def deadoralive():
    return render_template(
        'deadoralive.html'
        )

@app.route('/deadoralive_api', methods=['GET'])
def get_deadoralive():
    with open('deadoralive.json', 'r', encoding='utf-8') as f:
        deadoralive = json.load(f)

    time_now = int(time.time()/1)
    deadoralive['time_now'] = time_now

    former = deadoralive['21data_make']['21data_make0']
    latter = deadoralive['21data_make']['21data_make1']

    conpared = max(int(former), int(latter))
    diff = abs(int(conpared) - int(time_now))

    deadoralive['21data_make']['diff_now'] = diff
    res = jsonify(deadoralive)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

    app = Flask(__name__)