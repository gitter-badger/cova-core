# docker file for running compute node
FROM python:2.7

ADD ./ /cova-core
WORKDIR /cova-core

RUN pip install -r requirements.txt

EXPOSE 3051

CMD ["python", "core/run_server_node.py"]