from protocol_const import *
import time, thread, requests, json, random, hashlib, string
from collections import deque
from datetime import datetime
from sets import Set

MY_ID = 0
AVAILABILITY_LIST = [True] * NUMBER_OF_COMPUTERS
AVAILABLE_COMPUTERS_DEQUE = deque()
WORKING_COMPUTERS_DEQUE = deque()
MY_TASK = {}
MY_SECRET = 0
FP = 0
PENDING_TASK = {}
CREDENTIALS = {}

UNDER_MY_WORKING = Set()

def set_secret(secret):
    global MY_SECRET
    MY_SECRET = str(secret)
    return 'Got Secret'

def init(my_id):
    global MY_ID, FP, CREDENTIALS
    MY_ID = my_id
    FP = open('Log/router.txt', 'a+', 0)

    address = 'http://localhost:5002/create_cred/' + str(MY_ID)

    CREDENTIALS = requests.get(address).text
    CREDENTIALS = json.loads(CREDENTIALS)

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
    global WORKING_COMPUTERS_DEQUE, MY_TASK
    if(len(MY_TASK) > 0):
        print(computer_id, localtime, task_id)
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
        random_router_id = random.randint(0, NUMBER_OF_ROUTERS - 1)
        router_address = give_me_router_address(random_router_id)
        router_address += '/search_available'
        computer_id = str(requests.post(router_address).text)
        if computer_id == 'None':
            continue
        return int(computer_id)

def task_id_generator():
    letters = string.ascii_lowercase
    random_string = str(int(time.time()))
    random_string += ''.join(random.choice(letters) for i in range(3))
    return random_string

def cost_function(timeout):
    return 100

def init_task(data_user_id, timeout, datahash):

    global PENDING_TASK
    task_id = task_id_generator()

    cost = cost_function(timeout)

    PENDING_TASK[task_id] = {'data_user_id' : data_user_id, 'cost' : cost, 'timeout' : timeout, 'datahash' : datahash}

    print(PENDING_TASK)

    return json.dumps({'task_id' : task_id, 'cost' : cost})

def check_for_agreement(data_user_id, task_id):

    global PENDING_TASK

    if task_id in MY_TASK:
        return True

    if task_id not in PENDING_TASK:
        print('Task Id Is not in Pending Task')
        return False

    address = 'http://localhost:5000/payment/seeAgreement/' + task_id

    print(address)

    try:
        ret = requests.get(address).text
    except:
        print('Could not connect to agreement')
        return False

    print(ret)

    try:
        ret = json.loads(ret)
    except:
        print('Could not convert')
        return False

    print(ret)

    if(int(str(ret['2']))<PENDING_TASK[task_id]['cost']):
        print('Agreement is not created')
        return False

    datahash = PENDING_TASK[task_id]['datahash']

    if(str(ret['1']) != datahash):
        print('Datahash is not same')
        return False

    return True

def get_data_link(datahash):
    global MY_ID

    address = 'http://localhost:5001/get_keyfrag/' + str(datahash) + '/' + str(MY_ID)

    try:
        ret = requests.get(address).text
    except:
        print('Cannot Get Datahash in get_data_link')
        return 'sad.com'

    ret = json.loads(ret)

    try:
        ret = ret['metadata']['metadata']['data_link']
    except:
        print('Cannot retrieve in get_data_link')
        return 'sad.com'

    return str(ret)

def give_me_key_fragments(datahash):

    start_node = random.randint(0, NUMBER_OF_ROUTERS - 1)
    ret = []

    for i in range(SECRET_NUM):
        router_id = (start_node + i) % NUMBER_OF_ROUTERS
        address = give_me_router_address(router_id)
        address += '/dec_key_fragment'
        dec_key_fragment = str(requests.post(address, data = {'datahash' : datahash}).text)
        ret.append(dec_key_fragment)

    return ret

def dec_key_fragment(datahash):

    global MY_ID

    address = 'http://localhost:5001/get_keyfrag/' + str(datahash) + '/' + str(MY_ID)

    try:
        ret = requests.get(address).text
    except:
        print('Key Fragment Getting Error')
        return datahash + str(MY_ID)

    ret = json.loads(ret)

    if not ret['success']:
        print('Key Fragment Not Present')
        return datahash + str(MY_ID)

    ret = str(ret['keyfrag'])

    address = 'http://localhost:5002/decrypt'

    try:
        private_key = str(CREDENTIALS['rsa_cred']['privateKey'])
    except:
        print('Private Key Parsing Error')
        return datahash + str(MY_ID)

    try:
        ret = str(requests.post(address, data = {'enc_data' : ret, 'private_key' : private_key}).text)
    except:
        print('Decryption Error')
        return datahash + str(MY_ID)

    return ret

def new_task(data_user_id, task_id):

    if not check_for_agreement(data_user_id, task_id):
        return 'None'

    global UNDER_MY_WORKING, MY_TASK, PENDING_TASK

    if task_id in MY_TASK:
        cost = MY_TASK[task_id]['cost']
        timeout = MY_TASK[task_id]['timeout']
        datahash = MY_TASK[task_id]['datahash']
    elif task_id in PENDING_TASK:
        cost = PENDING_TASK[task_id]['cost']
        timeout = PENDING_TASK[task_id]['timeout']
        datahash = PENDING_TASK[task_id]['datahash']
    else:
        print('DataHash Not Found in Routing Node')
        return 'None'

    computer_id = search_for_available_computer()

    key_fragments = give_me_key_fragments(datahash)
    key_fragments = json.dumps(key_fragments)
    data_link = get_data_link(datahash)

    UNDER_MY_WORKING.add(computer_id)
    computer_address = give_me_computer_address(computer_id)
    computer_address += '/new_task/'
    computer_address += str(MY_ID)

    MY_TASK[task_id] = {'data_user_id' : data_user_id, 'computer_id' : computer_id, 'heartbeat' : give_me_time_counter(), 'datahash' : datahash, 'cost' : cost, 'timeout' : timeout}

    if task_id in PENDING_TASK:
        PENDING_TASK.pop(task_id)

    try:
        requests.post(computer_address, data = {'task_id' : str(task_id), 'datahash' : datahash, 'key_fragments' : str(key_fragments), 'data_link' : str(data_link)})
    except:
        MY_TASK.pop(task_id)
        new_task(data_user_id, task_id)
        return

    FP.write(give_me_time() + 'ROUTER ' + str(MY_ID) + ' Assigning task id ' + str(task_id) + ' to computer id ' + str(computer_id) + '\n')
    
    routers = give_me_random_routers(computer_id)
    
    for router in routers:
        router_address = give_me_router_address(router)
        router_address += '/computer/work/'
        router_address += str(computer_id)
        requests.post(router_address)

    return str(computer_id)
    

def end_task(task_id, return_value, notify_data_user = True):

    global UNDER_MY_WORKING, MY_TASK

    computer_id = MY_TASK[task_id]['computer_id']
    data_user_id = MY_TASK[task_id]['data_user_id']
    cost = MY_TASK[task_id]['cost']
    timeout = MY_TASK[task_id]['timeout']
    datahash = MY_TASK[task_id]['datahash']

    UNDER_MY_WORKING.remove(computer_id)

    if not notify_data_user:
        PENDING_TASK[task_id] = {'data_user_id' : data_user_id, 'cost' : cost, 'timeout' : timeout, 'datahash' : datahash}

    MY_TASK.pop(task_id)

    FP.write(give_me_time() + 'ROUTER ' + str(MY_ID) + ' Ending task id ' + str(task_id) + ' from computer id ' + str(computer_id) + '\n')
    
    routers = give_me_random_routers(computer_id)
    
    for router in routers:
        router_address = give_me_router_address(router)
        router_address += '/computer/finish/'
        router_address += str(computer_id)
        requests.post(router_address)

    if notify_data_user:
        data_user_address = give_me_data_user_address(data_user_id)
        data_user_address += '/end_task'
        requests.post(data_user_address, data = {'task_id' : str(task_id), 'return_value' : str(return_value)})


def reassign_task(computer_id, data_user_id, task_id):
    FP.write(give_me_time() + 'ROUTER ' + str(MY_ID) + ' Reassigning task id ' + str(task_id) + '\n')
    end_task(task_id, 'nothing', False)

    data_user_address = give_me_data_user_address(data_user_id)
    data_user_address += '/restart_task'

    requests.post(data_user_address, data = {'task_id' : task_id})

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
