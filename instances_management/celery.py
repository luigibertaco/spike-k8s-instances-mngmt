import os
from celery import Celery

app = Celery("tasks", backend="rpc://", broker="amqp://guest:guest@rabbitmq:5672")


@app.task
def add(x, y):
    worker = os.environ.get("WORKER_NAME")
    return f"{x + y} - {worker}"
