# docker file for running compute node
FROM python:2.7

ADD ../../ ./

RUN pip install -r requirements.txt


CMD ["python", "core/compute_node_server.py"]