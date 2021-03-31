import time
from typing import Optional

from fastapi import FastAPI

from .max_prime import max_prime_factors
from .celery import add

from kubernetes import client, config

app = FastAPI()


@app.get("/")
def read_root():
    task = add.delay(3, 4)
    return {"Hello": "World", "task": task.id, "pods": [pod for pod in list_pods()]}


@app.get("/items/{number}")
def read_item(number: int, queue: Optional[str] = None):
    start_time = time.perf_counter()
    max_prime = max_prime_factors(number)
    return {
        "number": number,
        "max_prime_factors": max_prime,
        "queue": queue,
        "time_calculating": time.perf_counter() - start_time,
    }


def list_pods():
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        yield {
            "ip": i.status.pod_ip,
            "ns": i.metadata.namespace,
            "name": i.metadata.name,
        }
