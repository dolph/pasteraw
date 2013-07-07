import fabric.api as fab


def vagrant():
    # grab vagrant's ssh config information
    ssh_config = fab.local('vagrant ssh-config', capture=True)
    # split the config so we can index into it (will break for multiple hosts)
    ssh_config = [line.strip() for line in ssh_config.split('\n')]
    ssh_config = dict(tuple(line.split(None, 1)) for line in ssh_config)
    # paths are wrapped with double quotes, which we don't need
    ssh_config = dict((k, v.strip('"')) for k, v in ssh_config.iteritems())

    fab.env.user = ssh_config['User']
    fab.env.hosts = ['%s:%s' % (ssh_config['HostName'], ssh_config['Port'])]
    fab.env.key_filename = ssh_config['IdentityFile']


def uname():
    fab.run('uname -a')


def setup():
    apt_dependencies = [
        'apache2',
        'libapache2-mod-wsgi',
        'python-setuptools']

    fab.sudo('apt-get update')
    fab.sudo('apt-get install -y %s' % ' '.join(apt_dependencies))

    # clean up apache2 install
    fab.sudo('rm -f /etc/apache2/sites-enabled/000-default')
    fab.sudo('rm -f /var/www/index.html')

    # setup our flask app
    fab.put('config/apache2/flaskr.wsgi', '/var/www/', use_sudo=True)
    fab.put(
        'config/apache2/flaskr',
        '/etc/apache2/sites-available/',
        use_sudo=True)
    fab.sudo('a2ensite flaskr')


def pack():
    # create a new source distribution as tarball
    fab.local('python setup.py sdist --formats=gztar', capture=False)


def deploy():
    # figure out the release name and version
    dist = fab.local('python setup.py --fullname', capture=True).strip()

    # upload the source tarball to the temporary folder on the server
    fab.put('dist/%s.tar.gz' % dist, '/tmp/flaskr.tar.gz')

    # create a place where we can unzip the tarball, then enter that directory
    # and unzip it
    fab.run('mkdir -p /tmp/flaskr')
    with fab.cd('/tmp/flaskr'):
        fab.run('tar xzf /tmp/flaskr.tar.gz')
        fab.run('ls -R')
        with fab.cd('/tmp/flaskr/%s' % dist):
            fab.sudo('python setup.py install')
    fab.sudo('rm -rf /tmp/flaskr /tmp/flaskr.tar.gz')
    fab.sudo('service apache2 reload')
