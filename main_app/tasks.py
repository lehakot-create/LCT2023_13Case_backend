from celery import shared_task


@shared_task
def my_task():
    print('Test task')
