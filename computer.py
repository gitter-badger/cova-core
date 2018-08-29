from flask import Flask, request, render_template
import time, thread, sys, requests
import computer_protocol
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World at port ' + sys.argv[1]
    
@app.route('/life')
def life_get():
    if computer_protocol.IS_ALIVE:
        return render_template('computer_life.html', LIFE_STATUS = 'Alive')
    else:
        return render_template('computer_life.html', LIFE_STATUS = 'Dead')

@app.route('/life', methods = ['POST'])
def life_post():
    computer_protocol.IS_ALIVE = not computer_protocol.IS_ALIVE
    return 'Altered!'

@app.route('/work', methods = ['POST'])
def work_post():
    computer_protocol.goto_work(int(request.form['router_id']))
    return 'went to work'

@app.route('/finish', methods = ['POST'])
def free_post():
    computer_protocol.finish_work()
    return 'finished work'

def init():
    computer_protocol.run(int(sys.argv[1]) - 5100)

def flaskThread():
    app.run(port = sys.argv[1])
    
if __name__ == "__main__":
    thread.start_new_thread(flaskThread, ())
    thread.start_new_thread(init, ())
    while True:
        pass
