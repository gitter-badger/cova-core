import requests, time, os, signal

def new_task(router_id, task_id, code_bin):
    return int(str(requests.post('http://localhost:' + str(5200) + '/new_task/' + str(task_id) + '/' + str(router_id), data = {'code_bin' : code_bin}).text))

def load_code(file_path):
    fp = open(file_path, 'r')
    return fp.read()

FP = open('../computer_logs.txt', 'r')

COMPUTER_ID = FP.read().split()
COMPUTER_ID = [int(i) for i in COMPUTER_ID]

def kill_computer(computer_id):
    os.kill(COMPUTER_ID[computer_id + 1], signal.SIGKILL)

task_id = 'noor148'

code_bin = load_code('data_user_code.py')

now_computer = new_task(0, task_id, code_bin)

print(now_computer)
