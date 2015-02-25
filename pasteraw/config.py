import uuid


DEBUG = False
TESTING = False
LOG_FILE = '/tmp/pasteraw.log'

# if you don't override the secret key, one will be chosen for you
SECRET_KEY = uuid.uuid4().hex

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

CLOUD_ID_TYPE = None
CLOUD_REGION = None
RACKSPACE_USERNAME = None
RACKSPACE_API_KEY = None
CDN_CONTAINER_NAME = 'pasteraw'
