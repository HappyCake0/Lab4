import json


def round_stats(data):
    for elem in data:
        for i in get_from_config("stats_names"):
            elem['data'][i] = round(float(elem['data'][i]), 2)
    return data


def read_stat(date):
    with open(f"/app/stats/{date}.json", 'r') as f:
        stats = f.read()

    data = json.loads(f"[{stats[:-1]}]")
    return round_stats(data)


def get_from_config(param):
    with open("config.json", 'r') as f:
        datastr = f.read()

    data = json.loads(datastr)
    value = data[f'{param}']
    return value


def approximate(data, measure):
    funcs = {
        "hour": approximate_to_hour,
        "day": approximate_to_day
    }
    if measure not in funcs:
        return 0
    return funcs[measure](data)


def approximate_to_hour(data):
    new_data = make_time(24)
    sorted_data = {}

    for i in range(0, 1440, 60):
        t = str(i / 60)[:-2] + "-00"
        if len(t) == 4:
            t = "0" + t
        sorted_data[t] = data[i:i + 60]
    stats_names = get_from_config('stats_names')
    for hour in new_data:
        for minute in sorted_data[hour["time"]]:
            for i in stats_names:
                hour["data"][i] += minute["data"][i]
        for i in stats_names:
            hour["data"][i] /= 60
    return round_stats(new_data)


def approximate_to_day(data):
    new_data = make_time(1)
    sorted_data = approximate_to_hour(data)
    stats_names = get_from_config('stats_names')
    for day in new_data:
        for element in sorted_data:
            for i in stats_names:
                day['data'][i] += element["data"][i]
        for i in stats_names:
            day['data'][i] /= 60
    return round_stats(new_data)


def make_time(amount):
    new_data = []
    for i in range(0, amount):
        t = str(i)
        if len(t) == 1:
            t = '0' + t
        stat = {
            "time": f"{t}-00",
            "data": {
                "memory": 0.0,
                "CPU_t": 0.0,
                "CPU_N": 0.0,
                "GPU_t": 0.0,
                "GPU_N": 0.0
            }
        }
        new_data.append(stat)
    return new_data

