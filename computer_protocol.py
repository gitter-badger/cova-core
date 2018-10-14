from protocol_const import *
import time, thread, requests, importlib

HEARTBEAT_ROUTERS = []
MY_ID = 0
IS_WORKING = False
MY_TASK_ID = 0
FP = 0
MY_ROUTER_ID = 0

def init(my_id):
    global MY_ID, HEARTBEAT_ROUTERS, IS_WORKING, FP
    IS_WORKING = False
    MY_ID = my_id
    HEARTBEAT_ROUTERS = give_me_random_routers(MY_ID)
    FP = open('Log/computer.txt', 'a+', 0)

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

def temp_working(code_bin):
    file_name = 'Code/code' + str(MY_ID) + '.py'
    code_fp = open(file_name, 'w+')
    code_fp.write(code_bin)
    code_fp.close()

    module_name = 'Code.code' + str(MY_ID)

    user_module = importlib.import_module(module_name)

    user_module.main()

    ret_fp = open('Code/output.txt', 'r')

    return ret_fp.read()

def wait_for_work(router_id, task_id):
    global IS_WORKING, HEARTBEAT_ROUTERS, MY_TASK_ID, MY_ROUTER_ID
    IS_WORKING = True
    MY_TASK_ID = task_id
    MY_ROUTER_ID = router_id
    HEARTBEAT_ROUTERS = [router_id]

    FP.write(give_me_time() + 'COMPUTER ' + str(MY_ID) + ' Waiting task id ' + str(task_id) + ' from router id ' + str(router_id) + '\n')

def do_work(task_id, code):

    global IS_WORKING, HEARTBEAT_ROUTERS, MY_TASK_ID

    if(task_id != MY_TASK_ID):
        return

    FP.write(give_me_time() + 'COMPUTER ' + str(MY_ID) + ' Working task id ' + str(task_id) + '\n')

    ret = temp_working(code)

    FP.write(give_me_time() + 'COMPUTER ' + str(MY_ID) + ' Finished task id ' + str(task_id) + '\n')
    
    IS_WORKING = False
    HEARTBEAT_ROUTERS = give_me_random_routers(MY_ID)
    router_address = give_me_router_address(MY_ROUTER_ID)
    router_address += '/computer/end_task'
    requests.post(router_address, data = {'task_id' : str(task_id), 'return_value' : str(ret)})

def goto_work(task_id, code_bin):
    thread.start_new_thread(do_work, (task_id, code_bin))
    
def run(my_id):
    init(my_id)
    thread.start_new_thread(send_heartbeat, ())
    while True:
        pass
