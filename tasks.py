import celery
app = celery.Celery('example')


@celery.task(name="tasks.add")
def add(x,y):
    return x + y

@celery.task
def background_task(*args, **kwargs):
	# code
	# more code
