import setuptools


setuptools.setup(
    name='pasteraw',
    version='1.1',
    long_description=__doc__,
    packages=['pasteraw'],
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    install_requires=[
        'flask',
        'pyrax',
        'flask-wtf',
        'blinker'])
