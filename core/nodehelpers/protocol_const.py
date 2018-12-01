NUMBER_OF_ROUTERS = 5
HEARTBEAT_ROUTER_COUNT = 3
COMPUTER_HEARTBEAT_TIME = 5
HEARTBEAT_CLEAR_TIME = 15
WORKING_COMPUTER_DETECTION_TIME = 15
SECRET_NUM = 2
LOCAL = True
ROUTER_ADDRESS = ['localhost:10000', 'localhost:10001', 'localhost:10002', 'localhost:10003', 'localhost:100004']

give_me_router_address = lambda router_id : 'http://' + router_id
give_me_computer_address = lambda computer_id : 'http://' + computer_id
