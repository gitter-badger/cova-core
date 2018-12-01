import hashlib, time, string, random
from datetime import datetime
from protocol_const import *

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

        random_router.append(ROUTER_ADDRESS[now_router])
    
    return random_router

def give_me_time_counter():
    return int(time.mktime(datetime.now().timetuple()))

def give_me_time():
    nowtime = datetime.now()
    return str(nowtime.hour) + ':' + str(nowtime.minute) + ':' + str(nowtime.second) + ' '