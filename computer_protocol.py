from protocol_const import *
import time, thread, requests

HEARTBEAT_ROUTERS = []
MY_ID = 0
IS_WORKING = False
MY_TASK_ID = 0

def init(my_id):
    global MY_ID, HEARTBEAT_ROUTERS, IS_WORKING
    IS_WORKING = False
    MY_ID = my_id
    HEARTBEAT_ROUTERS = give_me_random_routers(MY_ID)

def send_heartbeat():
    while True:
        for router in HEARTBEAT_ROUTERS:
            router_address = give_me_router_address(router)
            if IS_WORKING:
                router_address += '/computer/workingheartbeat/'
            else:
                router_address += '/computer/heartbeat/'
            router_address += str(MY_ID)
            
            now_time = give_me_time_counter()
            
            if IS_WORKING:
                requests.post(router_address, data = {'localtime' : str(now_time), 'task_id' : str(MY_TASK_ID)})
            else:
                requests.post(router_address, data = {'localtime' : str(now_time)})
        
        time.sleep(COMPUTER_HEARTBEAT_TIME)

def temp_working(task_id):
    time.sleep(50)

def do_work(router_id, task_id):
    global IS_WORKING, HEARTBEAT_ROUTERS, MY_TASK_ID
    IS_WORKING = True
    MY_TASK_ID = task_id
    HEARTBEAT_ROUTERS = [router_id]

    temp_working(task_id)
    
    IS_WORKING = False
    HEARTBEAT_ROUTERS = give_me_random_routers(MY_ID)
    router_address = give_me_router_address(router_id)
    router_address += '/computer/end_task'
    requests.post(router_address, data = {'task_id' : str(task_id)})

def goto_work(router_id, task_id):
    thread.start_new_thread(do_work, (router_id, task_id))
    
def run(my_id):
    init(my_id)
    thread.start_new_thread(send_heartbeat, ())
    while True:
        pass
