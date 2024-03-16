from flask import Flask, request, jsonify, render_template
import json
import utils

name = 'main'
app = Flask(name, template_folder="static")
with open("config.json", "r") as j:
    cfg = json.loads(j.read())

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stats', methods=['GET', 'POST'])
def pars_request():
    data = request.get_json()
    res = utils.read_stat("2024-01-01")
    res = utils.approximate(res, "day")
    return jsonify(res)


if name == 'main':
    app.run(debug=cfg['debug'], host=cfg['host'], port=cfg['port'])


