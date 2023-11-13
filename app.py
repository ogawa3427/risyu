from flask import Flask, render_template
import os
import re
import requests
import json

app = Flask(__name__)

qur = '2023q3.json'

count = 0

with open(os.path.join(os.path.expanduser('~'), 'risyu', 'sv_admin', 'strodict.json'), 'r', encoding='utf-8') as f:
    strodict = json.load(f)

with open(os.path.join(os.path.expanduser('~'), 'risyu', 'sv_admin', 'weakdict.json'), 'r', encoding='utf-8') as f:
    weakdict = json.load(f)

with open(os.path.join(os.path.expanduser('~'), 'risyu', 'sv_admin', qur), 'r', encoding='utf-8') as f:
    rolelist = json.load(f)
keys_list = list(rolelist.keys())

@app.route('/')
def index():
    global count
    with open('recieved.json', 'r', encoding='utf-8') as f:
        recieved = json.load(f)

    theline = recieved['csv']
    asof = recieved['asof']

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