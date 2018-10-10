from flask import Flask, request, render_template
import time, thread, sys, requests
import data_user_protocol
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Data User : Hello, World at port ' + sys.argv[1]

@app.route('/new_task/<task_id>/<router_id>')
def new_task(task_id, router_id):
    computer_id = data_user_protocol.new_task(int(task_id), int(router_id))
    return str(computer_id)

@app.route('/end_task', methods = ['POST'])
def end_task():
	data_user_protocol.end_task(int(request.form['task_id']))
	return 'Got It'

@app.route('/get_all_task')
def get_all_task():
	return data_user_protocol.print_all_task()

def init():
    data_user_protocol.run(int(sys.argv[1]) - 5200)

def flaskThread():
    app.run(port = sys.argv[1])
    
if __name__ == "__main__":
    thread.start_new_thread(flaskThread, ())
    thread.start_new_thread(init, ())
    while True:
        pass
