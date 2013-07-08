import celery

import flaskr


def make_celery(app):
    c = celery.Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'])
    c.conf.update(app.config)

    TaskBase = c.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    c.Task = ContextTask

    return c


CELERY = make_celery(flaskr.app)
