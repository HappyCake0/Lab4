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


def get_GPU_t_stats(): #траблы, траблы, траблы....
    command = "nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        temperature = result.stdout.strip()
        return temperature


def get_CPU_N_stats():
    command = "awk '{u=$2+$4; t=$2+$4+$5; if (NR==1){u1=u; t1=t;} else print ($2+$4-u1) * 100 / (t-t1); }' <(grep 'cpu ' /proc/stat) <(sleep 1;grep 'cpu ' /proc/stat)"
    process = subprocess.Popen(["/bin/bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if float(output.decode()) > 1:
        return str(float(output.decode()) - 1)
    else:
        return str(float(output.decode()))


while True:
    filename = datetime.datetime.now().strftime("%Y-%m-%d.json")
    current_time = datetime.datetime.now()
    current_time = str(current_time).split(" ")[1][:5].replace(":", "-")
    print(current_time)
    RAM_data = get_RAM_stats()
    CPU_N_data = get_CPU_N_stats()
    GPU_t_data = get_GPU_t_stats()
    if RAM_data >= cfg['critical_stats']['memory']: #добавить ост. парам-ры
        print('panic')
    stats = {
        "time": current_time,
        "data": {
            "memory": RAM_data,
            "CPU_t": "10",
            "CPU_N": CPU_N_data,
            "GPU_t": GPU_t_data,
            "GPU_N": "30"
        }
    }
    with open(f"stats/{filename}", "a+") as f:
        f.write(json.dumps(stats))
        f.write(',')
    time.sleep(2)
