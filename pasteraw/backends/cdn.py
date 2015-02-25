import hashlib

import pyrax

import pasteraw
from pasteraw import base36


ENABLED = False


if pasteraw.app.config['CLOUD_ID_TYPE'] == 'rackspace':
    pyrax.set_setting('identity_type', pasteraw.app.config['CLOUD_ID_TYPE'])
    print('Logging into rackspace as %s ...' %
          pasteraw.app.config['RACKSPACE_USERNAME'])
    pyrax.set_credentials(
        pasteraw.app.config['RACKSPACE_USERNAME'],
        pasteraw.app.config['RACKSPACE_API_KEY'])
elif pasteraw.app.config['CLOUD_ID_TYPE'] == 'keystone':
    raise NotImplementedError(
        'pyrax does not document how to provide keystone credentials '
        '"directly".')
else:
    raise Exception(
        'No credential type provided for CDN services (CLOUD_ID_TYPE).')

print('Setting region to %s' % pasteraw.app.config['CLOUD_REGION'])
pyrax.set_setting('region', pasteraw.app.config['CLOUD_REGION'])
pyrax.set_setting('use_servicenet', True)

containers = pyrax.cloudfiles.list_containers()
print('Available containers: %s' % containers)

container_name = pasteraw.app.config['CDN_CONTAINER_NAME']
container = pyrax.cloudfiles.get_container(container_name)
if container:
    print('Cloud Files ready.')


def upload(content):
    content = content.encode('utf-8')
    hex_key = hashlib.sha1(content).hexdigest()
    key = base36.re_encode(hex_key, starting_base=16)
    obj = container.store_object(key, content)
    obj.change_content_type('text/plain; charset="utf-8"')
    return key
