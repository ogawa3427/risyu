from flask import Flask, render_template, redirect
import os
import re
import json
import csv
import time
from flask import jsonify
from flask import request
from markupsafe import Markup
import subprocess

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

with open('2024q1_dns.tsv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    dns = {row[0]: row[2]+row[3] for row in reader}

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

#20240517144602  76E10b.203      ＧＳ科目        論理学と数学の基礎（数学的発想法）      金3     小原　功任    全学生（共通教育科目に係る卒業要件未充足の2年以上優先） 70      130     37      105     22   21       0
#20240517144702  76E10b.203      ＧＳ科目        論理学と数学の基礎（数学的発想法）      金3     小原　功任    全学生（共通教育科目に係る卒業要件未充足の2年以上優先） 70      130     37      105     22   21       0
#20240517144802  76E10b.203      ＧＳ科目        論理学と数学の基礎（数学的発想法）      金3     小原　功任    全学生（共通教育科目に係る卒業要件未充足の2年以上優先） 70      130     37      105     22   21       0
#20240517144901  76E10b.203      ＧＳ科目        論理学と数学の基礎（数学的発想法）      金3     小原　功任    全学生（共通教育科目に係る卒業要件未充足の2年以上優先） 70      130     37      105     22   21       0

@app.route('/img/<string:id>')
def img(id):
    print(id)
    #fullname = dns[id]
    teiin = 0
    with open(f'rcsvs/risyu{id}.tsv', 'r', encoding='utf-8') as f:
        data_q1 = [line.strip().split('\t') for line in f]

    no_doubling = []
    seen = []
    for item in data_q1:
        if item[0] not in seen:
            no_doubling.append(item)
            seen.append(item[0])
    # 各リスト内で7から16の要素を抽出
    extracted_data = []
    for item in no_doubling:
        extracted_data.append([item[0]] + item[7:])
    
    print(extracted_data)

    averaged_data = []
    if len(extracted_data) > 240:
        # リストの値を30個に一個で間引く処理
        thinned_data = []
        for index, item in enumerate(extracted_data):
            if (index + 1) % 30 == 0:
                thinned_data.append(item)
    if False:
    # 10項目ごとにデータを平均化する処理
        temp_data = []
        for index, item in enumerate(extracted_data):
            temp_data.append(item[1:])
            if (index + 1) % 10 == 0 or index == len(extracted_data) - 1:
                # 各列の平均を計算
                averaged_row = [sum(col) / len(col) for col in zip(*temp_data)]
                # 平均化された行にIDを追加して最終リストに追加
                averaged_data.append([item[0]] + averaged_row)
                temp_data = []  # リセット

    averaged_list = []
    if len(averaged_data) > 0:
        for item in averaged_data:
            averaged_list.append([item[0]] + item[1:])
    else:
        averaged_list = extracted_data
    averaged_list = thinned_data
    return render_template(
        'img.html',
        id=id,
        data=averaged_list,
        fullname=data_q1[0][3]
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

def error():
    res = jsonify(
        {
            'status': 'error',
            'operation type': 'unknown',
            'message': 'in valid input',
            'data': ''
        }
    )
    res.headers.add('Access-Control-Allow-Origin', '*')
    res.status_code = 400
    return res

@app.route('/api', methods=['GET'])
def get_example():
    mode_value = request.args.get('mode', '')
    word = request.args.get('word', '')

    if mode_value == '':
        with open('output.tsv', 'r', encoding='utf-8') as f:
            received = f.read()
        res = jsonify(received)
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res
    elif mode_value == 'search':
        if re.match(r'^\d{12}$', word):
            matched_lines = []
            with open('2024q1.tsv', 'r', encoding='utf-8') as file:
                for line in file:
                    if word in line:
                        matched_lines.append(line.strip().split('\t'))
            res = jsonify(
                {
                    'status': 'success',
                    'operation type': 'search',
                    'message': 'found by yyyyMMddHHmm',
                    'data': matched_lines
                }
            )
            res.headers.add('Access-Control-Allow-Origin', '*')
            return res
        
        elif re.match(r'^[a-zA-Z0-9]{5,7}\.?[a-zA-Z0-9]{0,3}$', word):
            matched_lines = []
            nums = []
            with open('2024q1.tsv', 'r', encoding='utf-8') as file:
                for line in file:
                    if word in line:
                        s_line = line.strip().split('\t')
                        if s_line[1] not in nums:
                            nums.append(s_line[1])
                        else:
                            if len(nums) > 1:
                                res = jsonify(
                                    {
                                        'status': 'redirect',
                                        'operation type': 'search',
                                        'message': 'multiple classes found, please specify one',
                                        'data': nums
                                    }
                                )
                                res.headers.add('Access-Control-Allow-Origin', '*')
                                res.status_code = 300
                                return res
                        matched_lines.append(s_line)
                res = jsonify(
                    {
                        'status': 'success',
                        'operation type': 'search',
                        'message': 'found by class code',
                        'data': matched_lines
                    }
                )
                res.headers.add('Access-Control-Allow-Origin', '*')
                return res
            
        elif re.match(r'^\d{14}$', word):
            message = {'error':'this type of query must be 12 digits'}
            res = jsonify(
                {
                    'status': 'error',
                    'operation type': 'search',
                    'message': message,
                    'data': ''
                }
            )
            res.headers.add('Access-Control-Allow-Origin', '*')
            res.status_code = 400
            return res
        
        else:
            return error()
        
    elif mode_value == 'hackathon':
        matched_lines = []
        timestr = ''
        # 2 23 56
        # 3 23 57
        #現在時刻hhmmでを取得
        now = time.strftime('%H%M')
        #現在時刻hhmmをint型に変換
        now_ = int(now)
        now = str(now)
        if len(now) == 3:
            now = '0' + now
        if now_ < 2355:
            timestr = '20240403' + now
        else:
            timestr = '20240402' + now
        print(timestr)
        with open('2024q1.tsv', 'r', encoding='utf-8') as file:
            for line in file:
                if timestr in line:
                    matched_lines.append(line.strip().split('\t'))
        res = jsonify(
            {
                'status': 'success',
                'operation type': 'realtime',
                'message': 'thanks for participating in the hackathon',
                'data': matched_lines
            }
        )
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res

    elif mode_value == 'exchange' and re.match(r'^[a-zA-Z0-9]{5,7}\.?[a-zA-Z0-9]{0,3}$', word):
            print('exchange')
            matched_lines = []
            with open('2024q1_dns.tsv', 'r', encoding='utf-8') as f:
                received = f.read()
            lines = received.split('\n')
            for line in lines:
                if word in line:
                    matched_lines.append(line.strip().split('\t'))
            res = jsonify(
                {
                    'status': 'success',
                    'operation type': 'exchange',
                    'message': 'found by class code',
                    'data': matched_lines
                }
            )
            res.headers.add('Access-Control-Allow-Origin', '*')
            return res
    elif mode_value == 'all':
        with open('2024q1_dns.tsv', 'r', encoding='utf-8') as f:
            received = f.read()
        lines = received.strip().split('\n')
        tosend = []
        for line in lines:
            print(line)
            line = line.split('\t')
            tosend.append([line[0], line[2]])
        res = jsonify(
            {
                'status': 'success',
                'operation type': 'all',
                'message': 'all classes',
                'data': tosend
            }
        )
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res
    else:
        return error()


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