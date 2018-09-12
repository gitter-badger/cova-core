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
    computer_protocol.goto_work(int(router_id), int(request.form['task_id']))
    return 'went to work'

def init():
    computer_protocol.run(int(sys.argv[1]) - 5100)

def flaskThread():
    app.run(port = sys.argv[1])
    
if __name__ == "__main__":
    thread.start_new_thread(flaskThread, ())
    thread.start_new_thread(init, ())
    while True:
        pass
