import json


def round_stats(data):
    for elem in data:
        for i in get_from_config("stats_names"):
            elem['data'][i] = round(float(elem['data'][i]), 2)
    return data


def get_from_config(param):
    with open("config.json", 'r') as f:
        datastr = f.read()

    data = json.loads(datastr)
    value = data[f'{param}']
    return value


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
