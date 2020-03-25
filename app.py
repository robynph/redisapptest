# in app.py

import os

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

def make_celery(app):
	# set redis url vars
	app.config['CELERY_BROKER_URL'] = environ.get('REDIS_URL', 'redis://localhost:6379/0')
    app.config['CELERY_RESULT_BACKEND'] = app.config['CELERY_BROKER_URL']
    # create context tasks in celery
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(current_app)
