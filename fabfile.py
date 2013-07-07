import fabric.api as fab


def vagrant():
    def parse_result(result):
        return result.split()[1].strip('"')

    result = fab.local('vagrant ssh-config | grep User', capture=True)
    fab.env.user = parse_result(result)

    result = fab.local('vagrant ssh-config | grep Port', capture=True)
    port = parse_result(result)
    result = fab.local('vagrant ssh-config | grep HostName', capture=True)
    host = parse_result(result)
    fab.env.hosts = ['%s:%s' % (host, port)]

    result = fab.local('vagrant ssh-config | grep IdentityFile', capture=True)
    fab.env.key_filename = parse_result(result)


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

    fab.put('config/apache2/flaskr.wsgi', '/var/www/', use_sudo=True)
    fab.put(
        'config/apache2/flaskr',
        '/etc/apache2/sites-available/',
        use_sudo=True)
    fab.sudo('a2ensite flaskr')
    fab.sudo('service apache2 reload')
