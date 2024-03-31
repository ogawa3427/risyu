from flask import Flask, render_template, redirect
import os
import re
import json
import csv
import time
from flask import jsonify
from flask import request
from markupsafe import Markup

app = Flask(__name__)

qur = '2023q4.json'

app.json.ensure_ascii = False

csvs_directory = os.path.join(os.path.expanduser('~'), 'risyu', 'csvs')

count = 0

jb_dict = {
    '51_00': '学域共通',
    '51_01': '人文学類',
    '51_02': '法学類',
    '51_03': '経済学類',
    '51_04': '学校教育学類,学校教育学類共同教員養成課程',
    '51_05': '地域創造学類',
    '51_06': '国際学類',
    '51_99': '教職・資格'
}

rk_dict = {
    '52_00': '学域共通',
    '52_10': '理工一括',
    '52_01': '数物科学類',
    '52_02': '物質化学類',
    '52_11': '機械工学類',
    '52_12': 'フロンティア工学類',
    '52_13': '電子情報通信学類',
    '52_14': '地球社会基盤学類',
    '52_15': '生命理工学類',
    '52_99': '教職・資格'
}

md_dict = {
    '53_00': '学域共通',
    '53_01': '医学類',
    '53_03': '保健学類',
    '53_04': '薬学類',
    '53_05': '医薬科学類'
}

other_dict = {
    '00_00': '総合教育部',
    '--_--': '共通教育',
    '46_91': '国際機構'
}


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

with open("course_info.json", "r", encoding="utf-8") as f:
    course_info = json.load(f)

with open(os.path.join(os.path.expanduser('~'), 'risyu', 'sv_admin', 'depander.json'), 'r', encoding='utf-8') as f:
    parent_depander = json.load(f)
if (str(os.environ.get('RISYU_ENV')) == 'dev'):
    depander = parent_depander['dev']
    print('dev')
else:
    depander = parent_depander['prod']
    print('prod')

@app.route('/')
def index():
    global count
    with open(os.path.join(os.path.expanduser('~'), 'counter.txt'), 'w', encoding='utf-8') as f:
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
    with open('output.tsv', 'r', encoding='utf-8') as f:
        recieved = f.read()
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

@app.route('/tests')
def tests():
    return render_template(
        'tests.html'
        )

@app.route('/yugo_table')
def yugo_table():
    #try:
    iswith = request.args.get('yugo', "1")
    aff = request.args.get('aff', "52_13")
    iki = ""

    if "51_" in aff:
        iki = "人間社会学域"
        p_rui = jb_dict[aff]
    elif "52_" in aff:
        iki = "理工学域"
        p_rui = rk_dict[aff]
    elif "53_" in aff:
        iki = "医薬保健学域"
        p_rui = md_dict[aff]
    else:
        iki = "other"
        p_rui = other_dict[aff]

    if p_rui == "機械工学類":
        p_rui = "機械工学類（新）"


    filled = {}
    if p_rui == "理工一括":
        for key in course_info:
            if course_info[key]['rui'] == "理工一括":
                filled[key] = course_info[key]
    elif p_rui == "総合教育部":
        for key in course_info:
            if course_info[key]['iki'] == "総合教育部":
                filled[key] = course_info[key]
                filled[key]['rui'] = "総合教育部"
    elif "_00" in aff:
        rui = "学域共通"
        for key in course_info:
            if course_info[key]['iki'] == iki and course_info[key]['rui'] == rui:
                filled[key] = course_info[key]
    elif iki == "other":
        for key in course_info:
            #print("!--")
            #print(course_info[key]['rui'])
            #print(rui)
            if course_info[key]['iki'] == p_rui:
                filled[key] = course_info[key]
    else:
        ruis = p_rui.split(",")
        for rui in ruis:
            for key in course_info:
                #print("---")
                #print(course_info[key]['rui'])
                #print(rui)
                if course_info[key]['rui'] == rui:
                    filled[key] = course_info[key]
        #for key in course_info:
        #    if course_info[key]['iki'] == iki and course_info[key]['rui'] == aff:
        #        filled[key] = course_info[key]

    if iswith == "1":
        for key in course_info:
            if course_info[key]['iki'] == "融合学域":
                filled[key] = course_info[key]
    
    # course_infoをJSON文字列に変換
    to_send_json = json.dumps(filled, ensure_ascii=False)

    course_info_safe = Markup(to_send_json)
    course_info_safe = course_info_safe.replace('^\"', "")
    course_info_safe = course_info_safe.replace("\"$", "")

    #print(iki)
    #print(p_rui)

    return render_template(
        'yugo_table.html',
        course_info=course_info_safe,
        rui_name=p_rui
    )
    #except Exception as e:
   #     print(e)
   #     return redirect('/yugo_table?aff=52_13&yugo=1')
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

    app = Flask(__name__)