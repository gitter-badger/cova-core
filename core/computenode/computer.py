import time, thread, sys
import computer_protocol
from datetime import datetime
from nodehelpers import request_helper
from nodehelpers.address_helper import get_port


def hello():
    return 'Computer : Hello, World at port ' + sys.argv[1]

def new_task_post(router_id, form):
    computer_protocol.wait_for_work(str(router_id), str(form['task_id']), str(form['datahash']), str(form['data_link']))
    return 'waiting to work'

def goto_work(form):
    computer_protocol.goto_work(str(form['task_id']), str(form['code_bin']))
    return 'went to work'

get_req = {'hello' : ['/', 0]}
post_req = {'new_task_post' : ['/new_task', 1],
            'goto_work' : ['/goto_work', 0]}

request_helper.hello = hello
request_helper.new_task_post = new_task_post
request_helper.goto_work = goto_work

def init(my_id, address):
    computer_protocol.run(my_id, address)

def flaskThread(address):
    port = get_port(address)
    ob = request_helper.ManualRequest(get_req, post_req, port)
    ob.run()
    
def run(my_id, address):
    thread.start_new_thread(flaskThread, (address, ))
    thread.start_new_thread(init, (my_id, address ))
    while True:
        time.sleep(1000)
