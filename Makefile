ROOT_DIR ?= $(shell pwd)

init:
	pip install -r requirements.txt

test:
	nosetests tests

build:
	docker build -t cova-node -f dockerfiles/Dockerfile .

run_compute_node:
	docker run -v $(ROOT_DIR)/core/configs/usercred.json:/cova-core/core/configs/usercred.json -p 11001:3051 -t cova-node

run_routing_nodes:
	docker run -v $(ROOT_DIR)/core/routingnode/cred_router0.txt:/cova-core/core/configs/usercred.json -p 10000:3051 -t cova-node &
	docker run -v $(ROOT_DIR)/core/routingnode/cred_router1.txt:/cova-core/core/configs/usercred.json -p 10001:3051 -t cova-node &
	docker run -v $(ROOT_DIR)/core/routingnode/cred_router2.txt:/cova-core/core/configs/usercred.json -p 10002:3051 -t cova-node &
	docker run -v $(ROOT_DIR)/core/routingnode/cred_router3.txt:/cova-core/core/configs/usercred.json -p 10003:3051 -t cova-node &
	docker run -v $(ROOT_DIR)/core/routingnode/cred_router4.txt:/cova-core/core/configs/usercred.json -p 10004:3051 -t cova-node
