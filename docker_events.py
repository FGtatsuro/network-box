#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import shlex
import subprocess
# TODO: Use logging module/SysLogHandler or stdout with fluentd
import syslog

from docker import Client

DEVNULL = open(os.devnull, 'wb')

client = Client(base_url='unix://var/run/docker.sock')
# Ref. https://docs.docker.com/engine/reference/api/images/event_state.png
# Event example:
#{
#  "status": "stop",
#  "id": "6ebb5f0272498921a145f75648d636289c341023593d3b04e2736229817ba84e",
#  "from": "vagrant_iptables",
#  "Type": "container",
#  "Action": "stop",
#  "Actor": {
#    "ID": "6ebb5f0272498921a145f75648d636289c341023593d3b04e2736229817ba84e",
#    "Attributes": {
#      "com.docker.compose.config-hash": "b4b9305b84cdbd99eedb26ff7008c0323349a5e251aa75b83f2733d0d582ab59",
#      "com.docker.compose.container-number": "1",
#      "com.docker.compose.oneoff": "False",
#      "com.docker.compose.project": "vagrant",
#      "com.docker.compose.service": "iptables",
#      "com.docker.compose.version": "1.6.2",
#      "image": "vagrant_iptables",
#      "name": "iptables"
#    }
#  },
#  "time": 1459094099,
#  "timeNano": 1459094099704873500
#}

with open('iptables/rules') as f:
    iptables_rules = [l for l in f.read().split('\n') if l]
# TODO: Create class to handle iptables command
iptables_command = 'iptables'
iptables_check_command = '{0} -C'.format(iptables_command)
iptables_insert_command = '{0} -I'.format(iptables_command)
iptables_delete_command = '{0} -D'.format(iptables_command)

# TODO: Create class to handle events
def on_start(event):
    # Workaround: start event can happen several time when container starts.
    # Thus, checking process is needed to prevent duplication of iptables rules.
    for rule in iptables_rules:
        # FYI: http://stackoverflow.com/questions/11269575/how-to-hide-output-of-subprocess-in-python-2-7
        ret = subprocess.call(shlex.split('{0} {1}'.format(iptables_check_command, rule)), stdout=DEVNULL, stderr=subprocess.STDOUT)
        if ret != 0:
            command = '{0} {1}'.format(iptables_insert_command, rule)
            syslog.syslog(syslog.LOG_INFO, 'network_container:{0}'.format(command))
            subprocess.call(shlex.split(command))

def on_stop(event):
    for rule in iptables_rules:
        ret = subprocess.call(shlex.split('{0} {1}'.format(iptables_check_command, rule)), stdout=DEVNULL, stderr=subprocess.STDOUT)
        if ret == 0:
            command = '{0} {1}'.format(iptables_delete_command, rule)
            syslog.syslog(syslog.LOG_INFO, 'network_container:{0}'.format(command))
            subprocess.call(shlex.split(command))

event_handlers = {}
event_handlers['start'] = on_start
event_handlers['stop'] = on_stop

# TODO: Use library to handle event loop
# TODO: Use fluentd for logging
gen = client.events(filters={'event': ['start', 'stop'], 'name': 'iptables'})
while True:
    # wait till event is invoked.
    event = json.loads(next(gen))
    syslog.syslog(syslog.LOG_INFO, 'network_container:{0}'.format(event))
    handler = event_handlers.get(event['status'])
    if handler:
        handler(event)
