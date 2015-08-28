import pyrax
import pyrax.exceptions

from pasteraw import app


ENABLED = False

if app.config['CLOUD_ID_TYPE'] == 'rackspace':
    try:
        pyrax.set_setting('identity_type', app.config['CLOUD_ID_TYPE'])

        app.logger.info(
            'Setting region to %s' % app.config['CLOUD_REGION'])
        pyrax.set_setting('region', app.config['CLOUD_REGION'])
        pyrax.set_setting('use_servicenet', True)

        app.logger.info(
            'Logging into rackspace as %s ...' %
            app.config['RACKSPACE_USERNAME'])
        pyrax.set_credentials(
            app.config['RACKSPACE_USERNAME'],
            app.config['RACKSPACE_API_KEY'])

        # list containers to exercise credentials
        pyrax.cloudfiles.list_containers()

        ENABLED = True
    except (pyrax.exceptions.PyraxException, AttributeError) as e:
        app.logger.warning(
            'Unable to authenticate using pyrax: %s' % e)
elif app.config['CLOUD_ID_TYPE'] == 'keystone':
    raise NotImplementedError(
        'pyrax does not document how to provide keystone credentials '
        '"directly".')
else:
    app.logger.warning(
        'No credential type provided for CDN services (CLOUD_ID_TYPE).')


def upload(key, content):
    if not ENABLED:
        return False

    try:
        container = pyrax.cloudfiles.get_container(
            app.config['CDN_CONTAINER_NAME'])
    except pyrax.exceptions.ClientException as e:
        app.logger.warning(e)
        return False

    try:
        obj = container.store_object(key, content)
        obj.change_content_type('text/plain; charset="utf-8"')
        return True
    except pyrax.exceptions.ClientException as e:
        app.logger.warning(e)

    return False
