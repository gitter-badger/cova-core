from protocol_const import *
import time, thread, requests

MY_ID = 0
MY_TASKS = {}

def init(my_id):
    global MY_ID
    MY_ID = my_id

def new_task(task_id, router_id):
    global MY_TASKS
    router_address = give_me_router_address(router_id)
    router_address += '/data_user/new_task/'
    router_address += str(MY_ID)
    computer_id = str(requests.post(router_address, data = {'task_id' : str(task_id)}).text)
    MY_TASKS[task_id] = router_id

    return str(computer_id)

def end_task(task_id):
    global MY_TASKS
    MY_TASKS.pop(task_id)

def print_all_task():
    global MY_TASKS
    ret = 'All tasks : <br/>'
    for task_id in MY_TASKS:
        ret += 'Task Number : %d working at Router Number : %d <br/>' % (task_id, MY_TASKS[task_id])
    
    return ret

def run(my_id):
    init(my_id)
    while True:
        pass
