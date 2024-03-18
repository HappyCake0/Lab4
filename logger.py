import subprocess
import json
import time
import datetime
import smtplib

with open("config.json", "r") as j:
    cfg = json.loads(j.read())


def send_email(stats, encode='utf-8'):
    text = ""
    for i in stats['data']:
        text += i + ": " + str(stats['data'][i]) + '\n'
    subject = "got critical stats"
    to_addr = cfg['moder_email']
    from_addr = "ilya.chepurin.01@mail.ru"
    passwd = "hUWjCaEnAsVNtH8rxWnR"
    server = "smtp.mail.ru"
    port = 465
    charset = f'Content-Type: text/plain; charset={encode}'
    mime = 'MIME-Version: 1.0'
    body = "\r\n".join((f"From: {from_addr}", f"To: {to_addr}",
           f"Subject: {subject}", mime, charset, "", text))

    try:
        smtp = smtplib.SMTP_SSL(server, port)
        smtp.ehlo()
        smtp.login(from_addr, passwd)
        smtp.sendmail(from_addr, to_addr, body.encode(encode))
    except smtplib.SMTPException as err:
        print('Что - то пошло не так...')
        raise err
    finally:
        smtp.quit()


def get_RAM_stats():
    data = subprocess.check_output('vmstat -s', shell=True)
    data = data.decode('utf-8')
    data = data.split('\n')[:2]
    total = int(data[0].split('K')[0].replace(' ', ''))
    used = int(data[1].split('K')[0].replace(' ', ''))
    return str((used / total) * 100.0)


def get_GPU_t_stats(): #TODO добыть статы (в докере не видит драйвер)
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


def check_critical_stats(stats):
    for i in stats['data']:
        if stats['data'][i] >= cfg['critical_stats'][i]:
            send_email(stats)
            stats['data']['runned_procces'] = "" #TODO: добавить парсер всех имен процессов из ps -ef
            with open(f"criticalstats/{filename}", "a+") as f:
                f.write(json.dumps(stats))
                f.write(',')
            return 0


while True:
    filename = datetime.datetime.now().strftime("%Y-%m-%d.json")
    current_time = datetime.datetime.now()
    current_time = str(current_time).split(" ")[1][:5].replace(":", "-")
    print(current_time)
    RAM_data = get_RAM_stats()
    CPU_N_data = get_CPU_N_stats()
    GPU_t_data = get_GPU_t_stats()
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
    check_critical_stats(stats)
    with open(f"stats/{filename}", "a+") as f:
        f.write(json.dumps(stats))
        f.write(',')
    time.sleep(10)


