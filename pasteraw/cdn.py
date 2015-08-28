import pyrax
import pyrax.exceptions

import pasteraw


ENABLED = False

if pasteraw.app.config['CLOUD_ID_TYPE'] == 'rackspace':
    try:
        pyrax.set_setting('identity_type', pasteraw.app.config['CLOUD_ID_TYPE'])

        pasteraw.app.logger.info(
            'Setting region to %s' % pasteraw.app.config['CLOUD_REGION'])
        pyrax.set_setting('region', pasteraw.app.config['CLOUD_REGION'])
        pyrax.set_setting('use_servicenet', True)

        pasteraw.app.logger.info(
            'Logging into rackspace as %s ...' %
            pasteraw.app.config['RACKSPACE_USERNAME'])
        pyrax.set_credentials(
            pasteraw.app.config['RACKSPACE_USERNAME'],
            pasteraw.app.config['RACKSPACE_API_KEY'])

        # list containers to exercise credentials
        pyrax.cloudfiles.list_containers()

        ENABLED = True
    except pyrax.exceptions.PyraxException as e:
        pasteraw.app.logger.warning(
            'Unable to authenticate using pyrax: %s' % e)

elif pasteraw.app.config['CLOUD_ID_TYPE'] == 'keystone':
    raise NotImplementedError(
        'pyrax does not document how to provide keystone credentials '
        '"directly".')
else:
    pasteraw.app.logger.warning(
        'No credential type provided for CDN services (CLOUD_ID_TYPE).')


def upload(key, content):
    if not ENABLED:
        return False

    try:
        container = pyrax.cloudfiles.get_container(
            pasteraw.app.config['CDN_CONTAINER_NAME'])
    except pyrax.exceptions.ClientException as e:
        pasteraw.app.logger.warning(e)
        return False

    try:
        obj = container.store_object(key, content)
        obj.change_content_type('text/plain; charset="utf-8"')
        return True
    except pyrax.exceptions.ClientException as e:
        pasteraw.app.logger.warning(e)

    return False
