import uuid


DEBUG = False
TESTING = False

# if you don't override the secret key, one will be chosen for you
SECRET_KEY = uuid.uuid4().hex

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
