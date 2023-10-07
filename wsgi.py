from flask import Flask, render_template
import os
import re

app = Flask(__name__)

@app.route('/')
def index():
    print("逆だったかもしれねえ、、、")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'risyu20230924235801.csv')
    asof = '2023年何月24日hh:mm現在'

    with open(file_path, 'r') as f:
        theline = ''.join(line for line in f if "時間割番号,科目区分" not in line)
        theline = re.sub('\n','eskape', theline)

    return render_template(
        'index.html',
        theline=theline,
        asof=asof
    )

@app.route('/set')
def set():
    return render_template('set.html')

@app.route('/aff')
def aff():
    rolelist = ['1年先導，観光デザイン，経済，地域，総合（文）優先', '履修条件あり（ピアノ経験者）', '１年地域優先', '１年人文，国際優先', '２年次以上限定', '１年生優先（2016年度以前入学生履修登録用）', '３年以上限定', '対象学生', '１年先導，観光デザイン人社学域・総合（文）優先', '１年先導，観光デザイン，経済，地域，総合（文）優先', '人文・法・国際限定，1年生優 先', '１年法優先', '3年生以上優先', '全学生（総合教育部学生優先）（英 語のみで受講可能な学生限定）', '２年以上限定', '１年生優先', '全学生（地域創造学類以外）（2021年度以前入学者履修登録用）', '２年以上優先', '理工学域優先', '全学生（国際学類をのぞく）', '全学生（総合教育部学生優先）', '３年以上優先', '未履修または「放棄」の２年生以上限定', '全学生', '全学生（地域創造学類以外）（2022年度以降入学者履修登録用）', '４年次以上限定（2019年度以前入学者履修登録用）', '１年人文，法，国際優先', '法学類の1年次以外限定', '全学生（2019年度以前入学者履修登録用）', ' 経済・地域・総合（文）限定，1年生優先', '全学生（2020年度以降入学者履 修登録用）', '全学生（地域創造学類優先，次いで融合学域・人文学類・法学類・経済学類・国際学類優先）', '２年生以上限定・未修得者のみ・３～４年生優先', '全学生（「超然文学賞」受賞者優先）', '１年先導・観光デザイン・経済・総合（文）優先']
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
    app.run()