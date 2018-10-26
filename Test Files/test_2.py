import requests, time, os, signal, json

def init_task(router_id, timeout, datahash):
    return requests.post('http://localhost:' + str(12000) + '/init_task/' + str(router_id), data = {'timeout' : timeout, 'datahash' : datahash}).text

def new_task(router_id, task_id):
    return int(str(requests.get('http://localhost:' + str(12000) + '/new_task/' + str(task_id) + '/' + str(router_id)).text))

def start_task(computer_id, task_id, code):
    requests.post('http://localhost:12000/start_task', data = {'computer_id' : str(computer_id), 'task_id' : str(task_id), 'code_bin' : str(code)})

def load_code(file_path):
    fp = open(file_path, 'r')
    return fp.read()

FP = open('../computer_logs.txt', 'r')

COMPUTER_ID = FP.read().split()
COMPUTER_ID = [int(i) for i in COMPUTER_ID]

def kill_computer(computer_id):
    os.kill(COMPUTER_ID[computer_id + 1], signal.SIGKILL)

datahash = 'nadimgukhay'

ret = json.loads(init_task(1, 15, datahash))

print(type(ret))
print(ret)

task_id = str(ret['task_id'])
cost = int(str(ret['cost']))

print(task_id, cost)

now_computer = new_task(1, task_id)

code = load_code('data_user_code.py')

start_task(now_computer, task_id, code)

print(now_computer)

time.sleep(15)

kill_computer(now_computer)
