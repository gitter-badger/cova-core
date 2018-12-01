# docker file for running routing node
FROM python:2.7

ADD ../../ ./

RUN pip install -r requirements.txt

EXPOSE 10000

CMD ["python", "core/routing_node_server.py"]