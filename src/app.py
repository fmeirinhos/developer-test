from flask import Flask, render_template, request, redirect, url_for
import os
import json
import tempfile
from backend import solve

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        mf_file = request.files['mf_file']
        e_file = request.files['e_file']

        mf_temp_path = tempfile.mktemp(suffix='.json')
        e_temp_path = tempfile.mktemp(suffix='.json')

        mf_file.save(mf_temp_path)
        e_file.save(e_temp_path)

        result = solve(mf_temp_path, e_temp_path)

        os.remove(mf_temp_path)
        os.remove(e_temp_path)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
