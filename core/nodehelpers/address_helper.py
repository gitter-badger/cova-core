import hashlib, time, string, random, json
from datetime import datetime
from protocol_const import *

ROUTER_ADDRESS = open('../configs/routing_node_public_credentials.txt', 'r')
ROUTER_ADDRESS = json.loads(ROUTER_ADDRESS.read())

def random_string():
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(10))
    return random_string

def give_me_random_routers(computer_id):

    random_router = []
    while len(random_router) < HEARTBEAT_ROUTER_COUNT:
        now_router = random.randint(0, NUMBER_OF_ROUTERS - 1)

        now_id = 'router' + str(now_router)

        if now_id in random_router:
            continue

        random_router.append(now_id)
    
    return random_router

def give_me_router_address(router_id):
    return 'http://' + str(ROUTER_ADDRESS[router_id]['public_ip'])

def give_me_time_counter():
    return int(time.mktime(datetime.now().timetuple()))

def give_me_time():
    nowtime = datetime.now()
    return str(nowtime.hour) + ':' + str(nowtime.minute) + ':' + str(nowtime.second) + ' '