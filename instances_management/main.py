import time
from typing import Optional

from fastapi import FastAPI

from .max_prime import max_prime_factors
from .celery import add

app = FastAPI()


@app.get("/")
def read_root():
    task = add.delay(3, 4)
    return {"Hello": "World", "task": task.id}


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
