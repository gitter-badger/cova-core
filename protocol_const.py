NUMBER_OF_ROUTERS = 3
NUMBER_OF_COMPUTERS = 100
HEARTBEAT_ROUTER_COUNT = 2
COMPUTER_HEARTBEAT_TIME = 5
HEARTBEAT_CLEAR_TIME = 15
WORKING_COMPUTER_DETECTION_TIME = 15
SECRET_NUM = 2
LOCAL = True

import hashlib, time, string, random
from datetime import datetime

def random_string():
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(10))
    return random_string

def give_me_random_routers(computer_id):

    random_router = []
    while len(random_router) < HEARTBEAT_ROUTER_COUNT:
        now_router = random.randint(0, NUMBER_OF_ROUTERS - 1)

        if now_router in random_router:
            continue

        random_router.append(now_router)
    
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
