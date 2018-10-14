import requests, time, os, signal

def new_task(router_id, task_id):
    return int(str(requests.get('http://localhost:' + str(5200) + '/new_task/' + str(task_id) + '/' + str(router_id)).text))

def start_task(computer_id, task_id, code):
    requests.post('http://localhost:5200/start_task', data = {'computer_id' : str(computer_id), 'task_id' : str(task_id), 'code_bin' : str(code)})

def load_code(file_path):
    fp = open(file_path, 'r')
    return fp.read()

FP = open('../computer_logs.txt', 'r')

COMPUTER_ID = FP.read().split()
COMPUTER_ID = [int(i) for i in COMPUTER_ID]

def kill_computer(computer_id):
    os.kill(COMPUTER_ID[computer_id + 1], signal.SIGKILL)

task_id = 'noor148'

now_computer = new_task(0, task_id)

code = load_code('data_user_code.py')

start_task(now_computer, task_id, code)

print(now_computer)

time.sleep(15)

kill_computer(now_computer)
