"""
Services for MQTT
"""

from core.misc.ipaddress import Ipv4Prefix
from core.service import CoreService


class Mosquitto(CoreService):
    """
    This is a sample user-defined service.
    """
    # a unique name is required, without spaces
    name = "Mosquitto"
    # you can create your own group here
    group = "IoT"
    # list executables that this service requires
    executables = ('/usr/sbin/mosquitto',)
    # list of other services this service depends on
    dependencies = ()
    # per-node directories
    dirs = ()
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    configs = ("mosquitto.conf",)
    # list of startup commands, also may be generated during startup
    startup = ("mosquitto -c mosquitto.conf -d",)
    # list of shutdown commands
    shutdown = ("pkill mosquitto",)

    @classmethod
    def generate_config(cls, node, filename):
        if filename == cls.configs[0]:
            return cls.generate_mosquitto_config(node)

    @classmethod
    def generate_mosquitto_config(cls, node):
        """
        Simple mosquitto config
        """
        cfg ="""
# =================================================================
# General configuration
# =================================================================

# Time in seconds to wait before resending an outgoing QoS=1 or
# QoS=2 message.
#retry_interval 20

# Time in seconds between updates of the $SYS tree.
# Set to 0 to disable the publishing of the $SYS tree.
#sys_interval 10

# Time in seconds between cleaning the internal message store of
# unreferenced messages. Lower values will result in lower memory
# usage but more processor time, higher values will have the
# opposite effect.
# Setting a value of 0 means the unreferenced messages will be
# disposed of as quickly as possible.
#store_clean_interval 10

# Write process id to a file. Default is a blank string which means
# a pid file shouldn't be written.
# This should be set to /var/run/mosquitto.pid if mosquitto is
# being run automatically on boot with an init script and
# start-stop-daemon or similar.
pid_file ""

# When run as root, drop privileges to this user and its primary
# group.
# Leave blank to stay as root, but this is not recommended.
# If run as a non-root user, this setting has no effect.
# Note that on Windows this has no effect and so mosquitto should
# be started by the user you wish it to run as.
user mosquitto

# =================================================================
# Default listener
# =================================================================

# IP address/hostname to bind the default listener to. If not
# given, the default listener will not be bound to a specific
# address and so will be accessible to all network interfaces.
# bind_address ip-address/host name
#bind_address

# Port to use for the default listener.
#port 1883

# The maximum number of client connections to allow. This is
# a per listener setting.
# Default is -1, which means unlimited connections.
# Note that other process limits mean that unlimited connections
# are not really possible. Typically the default maximum number of
# connections possible is around 1024.
#max_connections -1

# Choose the protocol to use when listening.
# This can be either mqtt or websockets.
# Websockets support is currently disabled by default at compile time.
# Certificate based TLS may be used with websockets, except that
# only the cafile, certfile, keyfile and ciphers options are supported.
#protocol mqtt

# When a listener is using the websockets protocol, it is possible to serve
# http data as well. Set http_dir to a directory which contains the files you
# wish to serve. If this option is not specified, then no normal http
# connections will be possible.
#http_dir

# Set use_username_as_clientid to true to replace the clientid that a client
# connected with with its username. This allows authentication to be tied to
# the clientid, which means that it is possible to prevent one client
# disconnecting another by using the same clientid.
# If a client connects with no username it will be disconnected as not
# authorised when this option is set to true.
# Do not use in conjunction with clientid_prefixes.
# See also use_identity_as_username.
#use_username_as_clientid


# =================================================================
# Persistence
# =================================================================

# If persistence is enabled, save the in-memory database to disk
# every autosave_interval seconds. If set to 0, the persistence
# database will only be written when mosquitto exits. See also
# autosave_on_changes.
# Note that writing of the persistence database can be forced by
# sending mosquitto a SIGUSR1 signal.
#autosave_interval 1800

# If true, mosquitto will count the number of subscription changes, retained
# messages received and queued messages and if the total exceeds
# autosave_interval then the in-memory database will be saved to disk.
# If false, mosquitto will save the in-memory database to disk by treating
# autosave_interval as a time in seconds.
#autosave_on_changes false

# Save persistent message data to disk (true/false).
# This saves information about all messages, including
# subscriptions, currently in-flight messages and retained
# messages.
# retained_persistence is a synonym for this option.
persistence false

# The filename to use for the persistent database, not including
# the path.
#persistence_file mosquitto.db

# Location for persistent database. Must include trailing /
# Default is an empty string (current directory).
# Set to e.g. /var/lib/mosquitto/ if running as a proper service on Linux or
# similar.
#persistence_location

# =================================================================
# Logging
# =================================================================

# Places to log to. Use multiple log_dest lines for multiple
# logging destinations.
# Possible destinations are: stdout stderr syslog topic file
#
# stdout and stderr log to the console on the named output.
#
# syslog uses the userspace syslog facility which usually ends up
# in /var/log/messages or similar.
#
# topic logs to the broker topic '$SYS/broker/log/<severity>',
# where severity is one of D, E, W, N, I, M which are debug, error,
# warning, notice, information and message. Message type severity is used by
# the subscribe/unsubscribe log_types and publishes log messages to
# $SYS/broker/log/M/susbcribe or $SYS/broker/log/M/unsubscribe.
#
# The file destination requires an additional parameter which is the file to be
# logged to, e.g. "log_dest file /var/log/mosquitto.log". The file will be
# closed and reopened when the broker receives a HUP signal. Only a single file
# destination may be configured.
#
# Note that if the broker is running as a Windows service it will default to
# "log_dest none" and neither stdout nor stderr logging is available.
# Use "log_dest none" if you wish to disable logging.
log_dest file mosquitto.log


# If using syslog logging (not on Windows), messages will be logged to the
# "daemon" facility by default. Use the log_facility option to choose which of
# local0 to local7 to log to instead. The option value should be an integer
# value, e.g. "log_facility 5" to use local5.
#log_facility

# Types of messages to log. Use multiple log_type lines for logging
# multiple types of messages.
# Possible types are: debug, error, warning, notice, information,
# none, subscribe, unsubscribe, websockets, all.
# Note that debug type messages are for decoding the incoming/outgoing
# network packets. They are not logged in "topics".
#log_type error
#log_type warning
#log_type notice
#log_type information

# Change the websockets logging level. This is a global option, it is not
# possible to set per listener. This is an integer that is interpreted by
# libwebsockets as a bit mask for its lws_log_levels enum. See the
# libwebsockets documentation for more details. "log_type websockets" must also
# be enabled.
#websockets_log_level 0

# If set to true, client connection and disconnection messages will be included
# in the log.
connection_messages true

# If set to true, add a timestamp value to each log message.
log_timestamp true

"""
        return cfg


class MQTTSN(CoreService):
    """
    This creates an MQTT-SN Gateway
    """
    # a unique name is required, without spaces
    name = "MQTT-SN-Gateway"
    # you can create your own group here
    group = "IoT"
    # list executables that this service requires
    executables = ('/usr/local/bin/MQTT-SNGateway',)
    # list of other services this service depends on
    dependencies = ()
    # per-node directories
    dirs = ()
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    configs = ("gateway.conf",)
    # list of startup commands, also may be generated during startup
    startup = ("MQTT-SNGateway -f gateway.conf",)
    # list of shutdown commands
    shutdown = ("pkill MQTT-SNGateway",)

    @classmethod
    def generate_config(cls, node, filename):
        if filename == cls.configs[0]:
            return cls.generate_mqttsn_config(node)

    @classmethod
    def generate_mqttsn_config(cls, node):
        """
        Simple gateway config
        """
        cfg ="""
#**************************************************************************
# Copyright (c) 2016, Tomoaki Yamaguchi
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# and Eclipse Distribution License v1.0 which accompany this distribution.
#
# The Eclipse Public License is available at
#    http://www.eclipse.org/legal/epl-v10.html
# and the Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#***************************************************************************

# config file of MQTT-SN Gateway

BrokerName=localhost
BrokerPortNo=1883
BrokerSecurePortNo=8883

ClientAuthentication=NO
#ClientsList=/path/to/your_clients.conf

PredefinedTopic=NO
#PredefinedTopicFile=/path/to/your_predefinedTopic.conf

#RootCAfile=/etc/ssl/certs/ca-certificates.crt
#RootCApath=/etc/ssl/certs/
#CertsFile=/path/to/certKey.pem
#PrivateKey=/path/to/privateKey.pem

GatewayID=1
GatewayName=PahoGateway-01
KeepAlive=900
#LoginID=your_ID
#Password=your_Password

# UDP
GatewayPortNo=10000
MulticastIP=225.1.1.1
MulticastPortNo=1883

# XBee
#Baudrate=38400
#SerialDevice=/dev/ttyUSB0
#ApiMode=2

# LOG
ShearedMemory=NO;

"""
        return cfg

class PahoBroker(CoreService):
    """
    This creates an MQTT broker in Python
    """
    # a unique name is required, without spaces
    name = "PahoBroker"
    # you can create your own group here
    group = "IoT"
    # list executables that this service requires
    executables = ()
    # list of other services this service depends on
    dependencies = ()
    # per-node directories
    dirs = ()
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    configs = ("udp.conf","paho-launch.sh",)
    # list of startup commands, also may be generated during startup
    startup = ("bash paho-launch.sh",)
    # list of shutdown commands
    shutdown = ()

    @classmethod
    def generate_config(cls, node, filename):
        if filename == cls.configs[0]:
            return cls.generate_PahoBroker_config(node)
        if filename == cls.configs[1]:
            return cls.generate_PahoBroker_launch(node)

    @classmethod
    def generate_PahoBroker_config(cls, node):
        """
        Simple gateway config
        """
        cfg ="""
loglevel debug

listener 1883

listener 1883 INADDR_ANY mqttsn

"""
        return cfg

    @classmethod
    def generate_PahoBroker_launch(cls, node):
        """
        Simple gateway config
        """
        cfg ="""#!/bin/sh
if [ -e /opt/paho.mqtt.testing/interoperability/startbroker.py ]; then
  python3 /opt/paho.mqtt.testing/interoperability/startbroker.py -c udp.conf > pahoBroker.log 2>&1 &
else
  echo "Can't find /opt/paho.mqtt.testing/interoperability/startbroker.py" > pahoBroker.log
  echo "please go to /opt and git clone https://github.com/eclipse/paho.mqtt.testing.git" >> pahoBroker.log
fi
"""
        return cfg

class MqttSnTools(CoreService):
    """
    This allows us to send and receive MQTT-SN messages
    """
    # a unique name is required, without spaces
    name = "MQTT-SN-tools"
    # you can create your own group here
    group = "IoT"
    # list executables that this service requires
    executables = ('/opt/mqtt-sn-tools/mqtt-sn-pub',)
    # list of other services this service depends on
    dependencies = ()
    # per-node directories
    dirs = ()
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    configs = ("mqtt-sn-tools.conf","message.txt","mqtt-sn-tools-launch.sh",)
    # list of startup commands, also may be generated during startup
    startup = ("bash mqtt-sn-tools-launch.sh mqtt-sn-tools.conf",)
    # list of shutdown commands
    shutdown = ("bash -c \'kill $(cat mqtt-sn-tools.pid)\'")

    @classmethod
    def generate_config(cls, node, filename):
        if filename == cls.configs[0]:
            return cls.generate_MqttSnTools_config(node)
        if filename == cls.configs[1]:
            return cls.generate_MqttSnTools_message(node)
        if filename == cls.configs[2]:
            return cls.generate_MqttSnTools_launch(node)

    @classmethod
    def generate_MqttSnTools_config(cls, node):
        """
        Send a message every 5 seconds
        """
        cfg ="5 10.0.1.1 1883 ${NODE_NAME:0:2} message.txt"
        return cfg

    @classmethod
    def generate_MqttSnTools_message(cls, node):
        """
        Message to send
        """
        cfg ="Hello World"
        return cfg

    @classmethod
    def generate_MqttSnTools_launch(cls, node):
        """
        Simple gateway config
        """
        cfg ="""#!/bin/bash
configfile="$1"
echo $$ > mqtt-sn-tools.pid
while IFS='' read -r line || [[ -n "$line" ]]; do
    # run the sender
    IFS=' ' read -r -a config <<< "$line"
    seconds=${config[0]}
    host=${config[1]}
    port=${config[2]}
    topic=${config[3]}
    export topic
    topic=$(bash -c "echo ${topic}")
    data=${config[4]}
    if [ -n "$seconds" ]; then
        while true; do
            if [ -e $data ]; then
                message=$(cat $data)
            else
                export $data
                message=$(bash -c "echo ${data}")
            fi
            /opt/mqtt-sn-tools/mqtt-sn-pub -d -h $host -p $port -q -1 -t $topic -m "$message"
            sleep $seconds
       done
    fi
done < "$configfile"
"""
        return cfg
