import logging
import time
from typing import Optional

from celery.result import AsyncResult
from fastapi import FastAPI
from kubernetes import client, config

from .celery import add
from .celery import app as celery_app
from .create_deployment import (
    create_deployment,
    create_deployment_object,
    delete_deployment,
    update_deployment,
    TIERS,
)
from .max_prime import max_prime_factors

app = FastAPI()

executed_tasks = []


@app.get("/hello")
def read_root():
    task = add.delay(3, 4)
    executed_tasks.append(task)
    return {"Hello": "World", "task": task.id}


@app.get("/pods")
def read_pods():
    return {"pods": list_pods()}


@app.get("/tasks")
def read_tasks():
    res = []
    for task in executed_tasks:
        res.append({"task": task.id, "status": task.status, "result": task.result})
    return res


@app.get("/task/{task_id}")
def get_task_result(task_id: str):
    task = AsyncResult(task_id, app=celery_app)
    return {"task": task.id, "status": task.status, "result": task.result}


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


@app.get("/pod/new/{name}")
def create_worker(name: str):
    deployment_object = create_deployment_object(name)
    create_deployment(deployment_object)
    return {"pods": list_pods()}


@app.get("/pod/new/{name}/{tier}")
def create_worker_tier(name: str, tier: int):
    if tier not in TIERS:
        return {"error": f"tier {tier} doesn't exist, should be one of {TIERS}"}

    deployment_object = create_deployment_object(name, tier)
    create_deployment(deployment_object)
    return {"pods": list_pods()}


@app.get("/pod/update/{name}/{tier}")
def update_worker(name: str, tier: int):
    if tier not in TIERS:
        return {"error": f"tier {tier} doesn't exist, should be one of {TIERS}"}

    deployment_object = create_deployment_object(name, tier)
    update_deployment(deployment_object)
    return {"pods": list_pods()}


@app.get("/pod/delete/{name}")
def delete_worker(name: str):
    delete_deployment(name)
    return {"pods": list_pods()}


def list_pods():
    try:
        config.load_incluster_config()

        v1 = client.CoreV1Api()
        print("Listing pods with their IPs:")
        ret = v1.list_namespaced_pod(namespace="default", watch=False)
        pods = []
        for i in ret.items:
            pods.append(
                {
                    "ip": i.status.pod_ip,
                    "ns": i.metadata.namespace,
                    "name": i.metadata.name,
                }
            )
        return pods
    except Exception as exc:
        logging.error(exc)
