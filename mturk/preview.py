import flask
app = flask.Flask(__name__)

import render

@app.route('/<page_num>')
def hello(page_num):
    return render.render(int(page_num))
