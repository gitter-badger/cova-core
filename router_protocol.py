from protocol_const import *
import time, thread, requests
from collections import deque
from datetime import datetime
from sets import Set
from random import randint

MY_ID = 0
AVAILABILITY_LIST = [True] * NUMBER_OF_COMPUTERS
AVAILABLE_COMPUTERS_DEQUE = deque()
WORKING_COMPUTERS_DEQUE = deque()
MY_TASK = {}

UNDER_MY_WORKING = Set()

def init(my_id):
    global MY_ID
    MY_ID = my_id

def make_computer_available(computer_id):
    global AVAIBILITY_LIST
    AVAILABILITY_LIST[computer_id] = True
    
def make_computer_unavailable(computer_id):
    global AVAIBILITY_LIST
    AVAILABILITY_LIST[computer_id] = False

def process_heartbeat(computer_id, localtime):
    global AVAILABLE_COMPUTERS_DEQUE
    AVAILABLE_COMPUTERS_DEQUE.append((computer_id, localtime))

def process_working_heartbeat(computer_id, localtime, task_id):
    print(computer_id, localtime, task_id)
    global WORKING_COMPUTERS_DEQUE, MY_TASK
    WORKING_COMPUTERS_DEQUE.append((computer_id, localtime))
    MY_TASK[task_id]['heartbeat'] = localtime

def delete_expired_heartbeat():
    global AVAILABLE_COMPUTERS_DEQUE, WORKING_COMPUTERS_DEQUE
    while True:
        if AVAILABLE_COMPUTERS_DEQUE:
            now_heartbeat = AVAILABLE_COMPUTERS_DEQUE[0]
            if int(time.mktime(datetime.now().timetuple())) - now_heartbeat[1] > HEARTBEAT_CLEAR_TIME:
                AVAILABLE_COMPUTERS_DEQUE.popleft()
        
        if WORKING_COMPUTERS_DEQUE:
            now_heartbeat = WORKING_COMPUTERS_DEQUE[0]
            if int(time.mktime(datetime.now().timetuple())) - now_heartbeat[1] > HEARTBEAT_CLEAR_TIME:
                WORKING_COMPUTERS_DEQUE.popleft()

def give_me_available_computer():
    global AVAILABLE_COMPUTERS_DEQUE

    while AVAILABLE_COMPUTERS_DEQUE:
        now_heartbeat = AVAILABLE_COMPUTERS_DEQUE[0]
        if AVAILABILITY_LIST[now_heartbeat[0]]:
            return now_heartbeat[0]
        AVAILABLE_COMPUTERS_DEQUE.popleft()

    return None

def search_for_available_computer():

    computer_id = 'None'

    while True:
        random_router_id = randint(0, NUMBER_OF_ROUTERS - 1)
        router_address = give_me_router_address(random_router_id)
        router_address += '/search_available'
        computer_id = str(requests.post(router_address).text)
        if computer_id == 'None':
            continue
        return int(computer_id)

def new_task(data_user_id, task_id):

    print('Got New Task', task_id)

    global UNDER_MY_WORKING, MY_TASK

    computer_id = search_for_available_computer()

    UNDER_MY_WORKING.add(computer_id)
    computer_address = give_me_computer_address(computer_id)
    computer_address += '/new_task/'
    computer_address += str(MY_ID)

    MY_TASK[task_id] = {'data_user_id' : data_user_id, 'computer_id' : computer_id, 'heartbeat' : give_me_time_counter()}

    requests.post(computer_address, data = {'task_id' : str(task_id)})
    
    routers = give_me_random_routers(computer_id)
    
    for router in routers:
        router_address = give_me_router_address(router)
        router_address += '/computer/work/'
        router_address += str(computer_id)
        requests.post(router_address)

    return str(computer_id)
    

def end_task(task_id, notify_data_user = True):

    print('Ending Task ', task_id)

    global UNDER_MY_WORKING, MY_TASK

    computer_id = MY_TASK[task_id]['computer_id']
    data_user_id = MY_TASK[task_id]['data_user_id']

    UNDER_MY_WORKING.remove(computer_id)

    MY_TASK.pop(task_id)
    
    routers = give_me_random_routers(computer_id)
    
    for router in routers:
        router_address = give_me_router_address(router)
        router_address += '/computer/finish/'
        router_address += str(computer_id)
        requests.post(router_address)

    if notify_data_user:
        data_user_address = give_me_data_user_address(data_user_id)
        data_user_address += '/end_task'
        requests.post(data_user_address, data = {'task_id' : str(task_id)})


def reassign_task(computer_id, data_user_id, task_id):

    print('Reassiging Work')

    end_task(task_id, False)
    new_task(data_user_id, task_id)

def check_working_computers():

    while True:
        for task_id, task in MY_TASK.iteritems():
            now_time = give_me_time_counter()
            if now_time - task['heartbeat'] > WORKING_COMPUTER_DETECTION_TIME:
                reassign_task(task['computer_id'], task['data_user_id'], task_id)

        time.sleep(WORKING_COMPUTER_DETECTION_TIME)

def return_all_status():
    available_comp = Set()
    working_comp = Set()
    for heartbeat in AVAILABLE_COMPUTERS_DEQUE:
        if AVAILABILITY_LIST[heartbeat[0]]:
            available_comp.add(heartbeat[0])
    
    ret = "Available Computers :<br/>"
    for comp in available_comp:
        ret += "Computer No "
        ret += str(comp)
        ret += "<br/>"
    
    ret += "<br/><br/>Under Me Working :<br/>"
    
    for comp in UNDER_MY_WORKING:
        ret += "Computer No "
        ret += str(comp)
        ret += "<br/>"
    
    for heartbeat in WORKING_COMPUTERS_DEQUE:
        if heartbeat[0] in UNDER_MY_WORKING:
            working_comp.add(heartbeat[0])
    
    ret += "<br/><br/>Under Me Alive :<br/>"
    
    for comp in working_comp:
        ret += "Computer No "
        ret += str(comp)
        ret += "<br/>"
    
    return ret

def run(my_id):
    init(my_id)
    thread.start_new_thread(delete_expired_heartbeat, ())
    thread.start_new_thread(check_working_computers, ())
    while True:
        pass
