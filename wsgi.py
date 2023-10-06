from flask import Flask, render_template
import os
import re

app = Flask(__name__)

@app.route('/')
def index():
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
    rolelist = ["全学生","全学生（地域創造学類以外）","全学生（理工学域優先）"]
    return render_template('aff.html',sver='2023Q3', rolelist=rolelist)

if __name__ == "__main__":
    app.run()