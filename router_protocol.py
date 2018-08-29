from protocol_const import *
import time, thread, requests
from collections import deque
from datetime import datetime
from sets import Set

MY_ID = 0
AVAILABILITY_LIST = [True] * NUMBER_OF_COMPUTERS
AVAILABLE_COMPUTERS_DEQUE = deque()
WORKING_COMPUTERS_DEQUE = deque()
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

def process_working_heartbeat(computer_id, localtime):
    global WORKING_COMPUTERS_DEQUE
    WORKING_COMPUTERS_DEQUE.append((computer_id, localtime))

def start_working(computer_id):
    global UNDER_MY_WORKING
    UNDER_MY_WORKING.add(computer_id)
    computer_address = give_me_computer_address(computer_id)
    computer_address += '/work'
    requests.post(computer_address, data = {'router_id' : str(MY_ID)})
    
    routers = give_me_random_routers(computer_id)
    
    for router in routers:
        router_address = give_me_router_address(router)
        router_address += '/computer/work/'
        router_address += str(computer_id)
        requests.post(router_address)

def finish_working(computer_id):
    global UNDER_MY_WORKING
    UNDER_MY_WORKING.remove(computer_id)
    computer_address = give_me_computer_address(computer_id)
    computer_address += '/finish'
    requests.post(computer_address, data = {'router_id' : str(MY_ID)})
    
    routers = give_me_random_routers(computer_id)
    
    for router in routers:
        router_address = give_me_router_address(router)
        router_address += '/computer/finish/'
        router_address += str(computer_id)
        requests.post(router_address)

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
    while True:
        pass
