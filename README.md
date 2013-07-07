flaskr
======

An implementation of [Flask's
tutorial](http://flask.pocoo.org/docs/tutorial/introduction/).

Running
-------

If you don't have [Vagrant](http://www.vagrantup.com/) and
[Fabric](http://fabfile.org/) installed, start there first.

    $ vagrant up
    $ fab vagrant setup pack deploy
    $ open http://127.0.0.1:8000/
