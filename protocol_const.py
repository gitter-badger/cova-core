NUMBER_OF_ROUTERS = 5
NUMBER_OF_COMPUTERS = 10
HEARTBEAT_ROUTER_COUNT = 3
COMPUTER_HEARTBEAT_TIME = 5
HEARTBEAT_CLEAR_TIME = 15

import hashlib, time
from datetime import datetime

def give_me_random_routers(computer_id):

    random_router = []
    for _ in range(HEARTBEAT_ROUTER_COUNT):
        now_router = int('0x' + hashlib.sha1(str(computer_id)).hexdigest(), 0) % NUMBER_OF_ROUTERS
        random_router.append(now_router)
        computer_id = computer_id + 1
    
    return random_router

def give_me_router_address(router_id):
    return 'http://localhost:' + str(5000 + router_id)
    
def give_me_computer_address(computer_id):
    return 'http://localhost:' + str(5100 + computer_id)

def give_me_time_counter():
    return int(time.mktime(datetime.now().timetuple()))

