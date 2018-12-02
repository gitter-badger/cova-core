# docker file for running compute node
FROM python:2.7

COPY requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip install -r requirements.txt

ADD ./ /cova-core
WORKDIR /cova-core/core

EXPOSE 3051

CMD ["python", "run_server_node.py"]