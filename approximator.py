import utils
def approximate(data, measure):
    funcs = {
        "hour": approximate_to_hour,
        "day": approximate_to_day
    }
    if measure not in funcs:
        return 0
    return funcs[measure](data)


def approximate_to_hour(data):
    new_data = utils.make_time(24)
    sorted_data = {}

    for i in range(0, 1440, 60):
        t = str(i / 60)[:-2] + "-00"
        if len(t) == 4:
            t = "0" + t
        sorted_data[t] = data[i:i + 60]
    stats_names = utils.get_from_config('stats_names')
    for hour in new_data:
        for minute in sorted_data[hour["time"]]:
            for i in stats_names:
                hour["data"][i] += minute["data"][i]
        for i in stats_names:
            hour["data"][i] /= 60
    return utils.round_stats(new_data)


def approximate_to_day(data):
    new_data = utils.make_time(1)
    sorted_data = approximate_to_hour(data)
    stats_names = utils.get_from_config('stats_names')
    for day in new_data:
        for element in sorted_data:
            for i in stats_names:
                day['data'][i] += element["data"][i]
        for i in stats_names:
            day['data'][i] /= 60
    return utils.round_stats(new_data)
