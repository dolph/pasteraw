import uuid


DEBUG = False
TESTING = False
LOG_FILE = '/var/log/pasteraw.log'

# if you don't override the secret key, one will be chosen for you
SECRET_KEY = uuid.uuid4().hex

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
