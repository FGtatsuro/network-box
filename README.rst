network-box
===========

Container stack to provide router for host newtwork.

Supported platform
------------------

- Debian

Requirements
------------

The dependencies on other softwares/librarys for this project.

- Python(>= 2.7.9)
- docker-py(>= 1.7.2)
  - requirements.txt of this project
- Docker(>= 1.10.3)
- Docker Compose(>= 1.6.2)
- iptables(>= 1.4.21)

Recommended ones are here.

- Vagrant(>= 1.8.1)
- pkill

How to
------

Start containers and a helper process.

.. code:: bash

    $ vi iptables/rules # Add rules of iptables
    $ sudo python docker_events.py &
    $ docker-compose up -d

Stop them.

.. code:: bash

    $ docker-compose stop
    $ sudo pkill -f -e docker_events

Sandbox environment
-------------------

You can check the features on VM.

.. code:: bash

    $ vagrant up

    $ vagrant ssh client
    (client)$ ping 192.168.50.2 # Check connection to dockerhost

    $ vagrant ssh dockerhost
    (dockerhost)$ cd /vagrant
    (dockerhost)$ sudo python docker_events.py &
    (dockerhost)$ docker-compose up -d # After this, message from client will not be reached
