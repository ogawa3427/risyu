from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'risyu20230924235801.csv')

    with open(file_path, 'r') as f:
        theline = ''.join(line for line in f if "時間割番号,科目区分" not in line)

    return render_template(
        'index.html',
        theline=theline
    )

@app.route('/set')
def set():
    return render_template('set.html')

@app.route('/aff')
def aff():
    return render_template('aff.html')

if __name__ == "__main__":
    app.run()