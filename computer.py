from flask import Flask, request, render_template
import time, thread, sys, requests
import computer_protocol
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Computer : Hello, World at port ' + sys.argv[1]

@app.route('/new_task/<router_id>', methods = ['POST'])
def new_task_post(router_id):
    computer_protocol.wait_for_work(int(router_id), str(request.form['task_id']), str(request.form['datahash']), str(request.form['key_fragments']))
    return 'waiting to work'

@app.route('/goto_work', methods = ['POST'])
def goto_work():
    computer_protocol.goto_work(str(request.form['task_id']), str(request.form['code_bin']))
    return 'went to work'

def init():
    computer_protocol.run(int(sys.argv[1]) - 11000)

def flaskThread():
    app.run(host = '0.0.0.0', port = sys.argv[1])
    
if __name__ == "__main__":
    thread.start_new_thread(flaskThread, ())
    thread.start_new_thread(init, ())
    while True:
        pass
