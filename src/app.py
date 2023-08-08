from flask import Flask, render_template, request
import json
from backend import solve

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        mf_file = request.files['mf_file']
        e_file = request.files['e_file']

        mf_content = json.load(mf_file)
        e_content = json.load(e_file)

        result = solve(mf_content, e_content)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
