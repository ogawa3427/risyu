from risyu import app
from flask import render_template
import os

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
