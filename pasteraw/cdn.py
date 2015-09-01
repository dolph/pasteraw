import pyrax
import pyrax.exceptions

from pasteraw import app
from pasteraw import log


ENABLED = False

if app.config['CLOUD_ID_TYPE'] == 'rackspace':
    try:
        pyrax.set_setting('identity_type', app.config['CLOUD_ID_TYPE'])

        log.info('Setting region', region=app.config['CLOUD_REGION'])
        pyrax.set_setting('region', app.config['CLOUD_REGION'])
        pyrax.set_setting('use_servicenet', True)

        log.info(
            'Logging into Rackspace',
            username=app.config['RACKSPACE_USERNAME'],
            api_key=bool(app.config['RACKSPACE_API_KEY']))
        pyrax.set_credentials(
            app.config['RACKSPACE_USERNAME'],
            app.config['RACKSPACE_API_KEY'])

        ENABLED = True
    except (pyrax.exceptions.PyraxException, AttributeError) as e:
        log.warning('Unable to authenticate using pyrax', exception=e)
elif app.config['CLOUD_ID_TYPE'] == 'keystone':
    raise NotImplementedError(
        'pyrax does not document how to provide keystone credentials '
        '"directly".')
else:
    log.warning(
        'No credential type provided for CDN services (CLOUD_ID_TYPE).')


def upload(key, content):
    if not ENABLED:
        return False

    try:
        container = pyrax.cloudfiles.get_container(
            app.config['CDN_CONTAINER_NAME'])
    except pyrax.exceptions.ClientException as e:
        log.warning('Error getting CDN container', exception=e)
        return False

    try:
        obj = container.store_object(key, content)
        obj.change_content_type('text/plain; charset="utf-8"')
        return True
    except pyrax.exceptions.ClientException as e:
        log.warning('Error storing object', exception=e)

    return False
