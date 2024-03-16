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
    res = what_to_read(data['datetime-from'], data['datetime-to'], data['approximate'])
    #res = utils.read_stat("2024-01-01")
    #res = utils.approximate(res, "day")
    return jsonify(res)


def what_to_read(date_start, date_end, selector):
    funcs = {
        "min": read_mins,
        "hour": read_hours,
        "day": read_days,
        "week": read_weeks
    }
    return funcs[selector](date_start, date_end)


def read_mins(date_start, date_end):
    if date_start[:-3] != date_end[:-3]:
        return 0
    day = str(date_start[:-6])
    hour = int(str(date_start).split(":")[1].split("-")[0])
    mins_start = int(str(date_start).split(":")[1].split("-")[1])
    mins_end = int(str(date_end).split(":")[1].split("-")[1])
    data = utils.read_stat(day)
    records_to_read = mins_end - mins_start + 1
    record_start = hour * 60 + mins_start
    new_data = data[record_start:record_start+records_to_read]
    return new_data

def read_hours():
    return 0


def read_days():
    return 0


def read_weeks():
    return 0


if name == 'main':
    app.run(debug=cfg['debug'], host=cfg['host'], port=cfg['port'])
