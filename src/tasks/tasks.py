from time import sleep

from src.celery import celery_app


async def async_foo(a, b):
    sleep(15)
    print(a, b)


@celery_app.task(name="FOO", task_track_started=True)
def foo(a, b):
    from asyncio import run
    run(async_foo(a=a, b=b))


@celery_app.task(name="PING")
def ping():
    print("PONG")
