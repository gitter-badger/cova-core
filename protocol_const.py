NUMBER_OF_ROUTERS = 3
NUMBER_OF_COMPUTERS = 6
HEARTBEAT_ROUTER_COUNT = 2
COMPUTER_HEARTBEAT_TIME = 5
HEARTBEAT_CLEAR_TIME = 15
WORKING_COMPUTER_DETECTION_TIME = 15

import hashlib, time
from datetime import datetime

def give_me_random_routers(computer_id):

    random_router = []
    for _ in range(HEARTBEAT_ROUTER_COUNT):
        some_value = 'sdjlsgihlsiejjlgihlsie' + str(computer_id)
        now_router = int('0x' + hashlib.sha256(str(some_value)).hexdigest(), 0) % NUMBER_OF_ROUTERS
        random_router.append(now_router)
        computer_id = computer_id + 1
    
    return random_router

def give_me_router_address(router_id):
    return 'http://localhost:' + str(10000 + router_id)
    
def give_me_computer_address(computer_id):
    return 'http://localhost:' + str(11000 + computer_id)

def give_me_data_user_address(data_user_id):
    return 'http://localhost:' + str(12000 + data_user_id)

def give_me_time_counter():
    return int(time.mktime(datetime.now().timetuple()))

def give_me_time():
    nowtime = datetime.now()
    return str(nowtime.hour) + ':' + str(nowtime.minute) + ':' + str(nowtime.second) + ' '
