from flask import Flask, request, render_template
import time, thread, sys, requests
import router_protocol

app = Flask(__name__)

@app.route('/')
def hello():
    return 'noor<br/>tonmoy<br/>nadim<br/>neerjhor<br/>'
    
@app.route('/computer/heartbeat/<computer_id>', methods = ['POST'])
def heartbeat_from_computer(computer_id):
    router_protocol.process_heartbeat(int(computer_id), int(request.form['localtime']))
    return "Got Heartbeat"

@app.route('/computer/workingheartbeat/<computer_id>', methods = ['POST'])
def heartbeat_from_working_computer(computer_id):
    router_protocol.process_working_heartbeat(int(computer_id), int(request.form['localtime']))
    return "Got Heartbeat"

@app.route('/computer/work/<computer_id>')
def start_working(computer_id):
    router_protocol.start_working(int(computer_id))
    return 'Started Working Computer Number : ' + str(computer_id)

@app.route('/computer/work/<computer_id>', methods = ['POST'])
def start_working_post(computer_id):
    router_protocol.make_computer_unavailable(int(computer_id))
    return 'Computer is unavailable : ' + str(computer_id)

@app.route('/computer/finish/<computer_id>')
def finish_working(computer_id):
    router_protocol.finish_working(int(computer_id))
    return 'Finished Working Computer Number : ' + str(computer_id)

@app.route('/computer/finish/<computer_id>', methods = ['POST'])
def finish_working_post(computer_id):
    router_protocol.make_computer_available(int(computer_id))
    return 'Computer is available : ' + str(computer_id)

@app.route('/allstatus/')
def allstatus():
    return router_protocol.return_all_status()

def init():
    router_protocol.run(int(sys.argv[1]) - 5000)

def flaskThread():
    app.run(port = sys.argv[1])
    
if __name__ == "__main__":
    thread.start_new_thread(flaskThread, ())
    thread.start_new_thread(init, ())
    while True:
        pass
