import uuid


DEBUG = False
TESTING = False

# if you don't override the secret key, one will be chosen for you
SECRET_KEY = uuid.uuid4().hex
