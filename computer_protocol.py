from protocol_const import *
import time, thread, requests

IS_ALIVE = True
HEARTBEAT_ROUTERS = []
MY_ID = 0
IS_WORKING = False

def init(my_id):
    global MY_ID, HEARTBEAT_ROUTERS
    MY_ID = my_id
    HEARTBEAT_ROUTERS = give_me_random_routers(MY_ID)

def send_heartbeat():
    while True:
        if not IS_ALIVE:
            continue
        for router in HEARTBEAT_ROUTERS:
            router_address = give_me_router_address(router)
            if IS_WORKING:
                router_address += '/computer/workingheartbeat/'
            else:
                router_address += '/computer/heartbeat/'
            router_address += str(MY_ID)
            
            now_time = give_me_time_counter()
            
            requests.post(router_address, data = {'localtime' : str(now_time)})
        
        time.sleep(COMPUTER_HEARTBEAT_TIME)

def goto_work(router_id):
    global IS_WORKING, HEARTBEAT_ROUTERS
    IS_WORKING = True
    HEARTBEAT_ROUTERS = [router_id]

def finish_work():
    global IS_WORKING, HEARTBEAT_ROUTERS
    IS_WORKING = False
    HEARTBEAT_ROUTERS = give_me_random_routers(MY_ID)
    
def run(my_id):
    init(my_id)
    thread.start_new_thread(send_heartbeat, ())
    while True:
        pass
