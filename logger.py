import subprocess
import json
import time
import datetime

with open("config.json", "r") as j:
    cfg = json.loads(j.read())


def get_RAM_stats():
    data = subprocess.check_output('vmstat -s', shell=True)
    data = data.decode('utf-8')
    data = data.split('\n')[:2]
    total = int(data[0].split('K')[0].replace(' ', ''))
    used = int(data[1].split('K')[0].replace(' ', ''))
    return str((used / total) * 100.0)


while True:
    filename = datetime.datetime.now().strftime("%Y-%m-%d.json")
    current_time = datetime.datetime.now().strftime("%H-%m")
    RAM_data = get_RAM_stats()
    if RAM_data >= cfg['critical_stats']['memory']: #добавить ост. парам-ры
        print('panic')
    stats = {
        "time": current_time,
        "data": {
            "memory": RAM_data,
            "CPU_t": "10",
            "CPU_N": "70",
            "GPU_t": "15",
            "GPU_N": "30"
        }
    }
    with open(f"stats/{filename}", "a+") as f:
        f.write(json.dumps(stats))
        f.write(',')
    time.sleep(2)
