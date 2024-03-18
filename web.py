from flask import Flask, request, jsonify, render_template
import json
import utils
from datetime import datetime

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
    # res = utils.read_stat("2024-01-01")
    # res = utils.approximate(res, "day")
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
    if (date_start[:-3] != date_end[:-3]) | (date_start == "") | (date_end == ""):
        return utils.make_time(1)
    day = get_date_WT(date_start)
    hour = int(get_hour(date_start))
    mins_start = int(get_min(date_start))
    mins_end = int(get_min(date_end))
    data = utils.read_stat(day)
    records_to_read = mins_end - mins_start + 1
    record_start = hour * 60 + mins_start
    new_data = data[record_start:record_start + records_to_read]
    return new_data


def read_hours(date_start, date_end):
    if (date_start[:-6] != date_end[:-6]) | (date_start == "") | (date_end == ""):
        return utils.make_time(1)
    day = get_date_WT(date_start)
    hour_start = int(get_hour(date_start))
    hour_end = int(get_hour(date_end))
    records_to_read = hour_end - hour_start + 1
    data = utils.approximate(data=utils.read_stat(day), measure="hour")
    new_data = data[hour_start:hour_start + records_to_read]
    return new_data


def read_days(date_start, date_end):
    if get_date_WT(date_start) == get_date_WT(date_end):
        return utils.make_time(1)
    day_start = get_date_WT(date_start)
    days_amount = int(get_day(date_end)) - int(get_day(date_start)) + 1
    current_day = day_start
    new_data = []
    for i in range(days_amount):
        new_item = utils.approximate(data=utils.read_stat(current_day), measure="day")
        new_item[0]["time"] = "00-" + get_day(current_day)
        new_data.append(new_item[0])
        print(new_data)
        if int(get_day(current_day)) < 9:
            current_day = current_day[:-2] + "0" + str(int(get_day(current_day)) + 1)
        else:
            current_day = current_day[:-2] + str(int(get_day(current_day)) + 1)
    return new_data


def read_weeks(date_start, date_end):
    interval = (datetime.strptime(get_date_WT(date_end), '%Y-%m-%d').date()
                - datetime.strptime(get_date_WT(date_start), '%Y-%m-%d').date())
    interval_in_days = int(str(interval).split(" ")[0]) + 1
    if interval_in_days % 7 != 0:
        return utils.make_time(1)
    data = read_days(date_start, date_end)
    new_data = utils.make_time(int(interval_in_days/7))
    current_week = 0
    stats_names = utils.get_from_config('stats_names')
    for week in new_data:
        week["time"] = current_week
        for i in range(0, interval_in_days, 7):
            for j in range(7):
                for stat in stats_names:
                    week["data"][stat] += data[i+j]["data"][stat]
        for i in stats_names:
            week['data'][i] /= 7
        current_week += 1
    return new_data


def get_hour(date):
    hour = date.split(":")[1].split("-")[0]
    return hour


def get_min(date):
    min = date.split(":")[1].split("-")[1]
    return min


def get_day(date):
    if len(date) > 10:
        day = date.split(":")[0].split("-")[2]
    else:
        day = date.split("-")[2]
    return day


def get_date_WT(date):
    new_date = date[:-6]
    return new_date


def read_stat(date):
    with open(f"/app/stats/{date}.json", 'r') as f:
        stats = f.read()

    data = json.loads(f"[{stats[:-1]}]")
    return utils.round_stats(data)

if name == 'main':
    app.run(debug=cfg['debug'], host=cfg['host'], port=cfg['port'])
