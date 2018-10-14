from flask import Flask, request, render_template
import time, thread, sys, requests
import router_protocol

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Router : Hello, World at port ' + sys.argv[1]
    
@app.route('/computer/heartbeat/<computer_id>', methods = ['POST'])
def heartbeat_from_computer(computer_id):
    router_protocol.process_heartbeat(int(computer_id), int(request.form['localtime']))
    return "Got Heartbeat"

@app.route('/computer/workingheartbeat/<computer_id>', methods = ['POST'])
def heartbeat_from_working_computer(computer_id):
    router_protocol.process_working_heartbeat(int(computer_id), int(request.form['localtime']), str(request.form['task_id']))
    return "Got Heartbeat"

@app.route('/computer/work/<computer_id>', methods = ['POST'])
def start_working_post(computer_id):
    router_protocol.make_computer_unavailable(int(computer_id))
    return 'Computer is unavailable : ' + str(computer_id)

@app.route('/computer/finish/<computer_id>', methods = ['POST'])
def finish_working_post(computer_id):
    router_protocol.make_computer_available(int(computer_id))
    return 'Computer is available : ' + str(computer_id)

@app.route('/allstatus')
def allstatus():
    return router_protocol.return_all_status()

@app.route('/data_user/new_task/<data_user_id>', methods = ['POST'])
def new_task(data_user_id):
    computer_id = router_protocol.new_task(int(data_user_id), str(request.form['task_id']), str(request.form['code_bin']))
    return str(computer_id)

@app.route('/computer/end_task', methods = ['POST'])
def end_task():
    router_protocol.end_task(str(request.form['task_id']), str(request.form['return_value']))
    return 'Ended Task'

@app.route('/search_available', methods = ['POST'])
def search_available():
    return str(router_protocol.give_me_available_computer())

@app.route('/set_secret', methods = ['POST'])
def set_secret():
    return str(router_protocol.set_secret(str(request.form['secret'])))

def init():
    router_protocol.run(int(sys.argv[1]) - 5000)

def flaskThread():
    app.run(port = sys.argv[1])
    
if __name__ == "__main__":
    thread.start_new_thread(flaskThread, ())
    thread.start_new_thread(init, ())
    while True:
        pass
