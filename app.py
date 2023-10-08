from flask import Flask, render_template
import os
import re
import json

app = Flask(__name__)

@app.route('/')
def index():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csvs_directory = os.path.join(current_directory, 'csvs')
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
        theline = ''.join(line for line in f if "時間割番号,科目区分" not in line)
        theline = re.sub('\n','eskape', theline)

    asof = max(numlist)
    patt = r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})"
    repl = r"\1年\2月\3日\4:\5:\6現在"
    asof = re.sub(patt, repl, asof)

    rolelist = ['1年先導，観光デザイン，経済，地域，総合（文）優先', '履修条件あり（ピアノ経験者）', '１年地域優先', '１年人文，国際優先', '２年次以上限定', '１年生優先（2016年度以前入学生履修登録用）', '３年以上限定', '対象学生', '１年先導，観光デザイン人社学域・総合（文）優先', '１年先導，観光デザイン，経済，地域，総合（文）優先', '人文・法・国際限定，1年 生優 先', '１年法優先', '3年生以上優先', '全学生（総合教育部学生優先）（英語のみで受講可能な学生限定）', '２年以上限定', '１年生優先', '全学生（地域創造学類以外）（2021年度以前入学者履修登録用）', '２年以上優先', '理工学域優先', '全学生（国際学類をのぞく）', '全学生（総合教育部学生優先）', '３年以上優先', '未履修または「放棄」の２年生以上限定', '全学生', '全学生（地域創造学類以外）（2022年度以降入学者履修登録用）', '４年次以上限定（2019年度以前入学者履修登録用）', '１年人文，法，国際優先', '法学類の1年次以外限定', '全学生（2019年度以前入学者履修登録用）', ' 経済・地域・総合（文）限定，1年生優 先', '全学生（2020年度以降入学者履 修登録用）', '全学生（地域創造学類優先，次いで融合学域・人文学類・法学類・経済学類・ 国際学類優先）', '２年生以上限定・未修得者のみ・３～４年生優先', '全学生（「超然文学賞」受賞者優先）', '１年先導・観光デザイン・経済・総合（文）優先']
    weakdict = {
    "PHILLIPPSJEREMYDAVID": "PHILLIPPS",
    "GRUENEBERGPATRICK": "GRUENEBERG",
    "グローバル": "グロ",
    "インテグレーテッド": "インテグ",
    "物理の世界": "物理",
    "化学の世界": "化学",
    "エクササイズ&スポーツ": "E&S",
    "コミュニケーション": "コミュ",
    "パーソナリティ": "ﾊﾟｰｿﾅﾘﾃｨ",
    "ケーススタディ": "ｹｰｽｽﾀﾃﾞｨ",
    "論理学から見る世界": "見る世界",
    "クリティカル・シンキング": "ｸﾘﾃｨｶﾙｼﾝｷﾝｸﾞ"
    };
    strodict = {
    "社会と地域の課題":"鯱",
    "時代の社会学": "社",
    "時代の国際協力": "国",
    "時代の文学": "文",
    "時代の政治経済学": "政経",
    "異文化間": "異",
    "ﾊﾟｰｿﾅﾘﾃｨ心理学": "パソ心",
    "価値と情動の認知科学": "価値情",
    "論理学と数学の基礎": "論理学",
    "ｸﾘﾃｨｶﾙｼﾝｷﾝｸﾞ": "クリシン"
    };
    return render_template(
        'index.html',
        theline=theline,
        asof=asof,
        rolelist=rolelist,
        weakdict=weakdict,
        strodict=strodict
    )

@app.route('/set')
def set():
    return render_template('set.html')

@app.route('/aff')
def aff():
    rolelist = ['1年先導，観光デザイン，経済，地域，総合（文）優先', '履修条件あり（ピアノ経験者）', '１年地域優先', '１年人文，国際優先', '２年次以上限定', '１年生優先（2016年度以前入学生履修登録用）', '３年以上限定', '対象学生', '１年先導，観光デザイン人社学域・総合（文）優先', '１年先導，観光デザイン，経済，地域，総合（文）優先', '人文・法・国際限定，1年 生優 先', '１年法優先', '3年生以上優先', '全学生（総合教育部学生優先）（英 語のみで受講可能な学生限定）', '２年以上限定', '１年生優先', '全学生（地域創造学類以外）（2021年度以前入学者履修登録用）', '２年以上優先', '理工学域優先', '全学生（ 国際学類をのぞく）', '全学生（総合教育部学生優先）', '３年以上優先', '未履修または「放棄」の２年生以上限定', '全学生', '全学生（地域創造学類以外）（2022年度以降入学者履修登録用）', '４年次以上限定（2019年度以前入学者履修登録用）', '１年人文，法，国際優先', '法学類の1年次以外限定', '全学生（2019年度以前入学者履修登録用）', ' 経済・地域・総合（文）限定，1年生 優先', '全学生（2020年度以降入学者履 修登録用）', '全学生（地域創造学類優先，次いで融合学域・人文学類・法学類・経済学類 ・国際学類優先）', '２年生以上限定・未修得者のみ・３～４年生優先', '全学生（「超然文学賞」受賞者優先）', '１年先導・観光デザイン・経済・総合（文）優先']
    return render_template(
        'aff.html',
        rolelist=rolelist
        )

@app.route('/man')
def man():
    return render_template(
        'man.html'
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)