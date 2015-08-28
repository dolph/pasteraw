import uuid


CDN_ENDPOINT = 'http://cdn.pasteraw.com'

PASTE_DIR = None
LOG_FILE = '/tmp/pasteraw.log'

# if you don't override the secret key, one will be chosen for you
SECRET_KEY = uuid.uuid4().hex

CLOUD_ID_TYPE = None
CLOUD_REGION = None
RACKSPACE_USERNAME = None
RACKSPACE_API_KEY = None
CDN_CONTAINER_NAME = 'pasteraw'
