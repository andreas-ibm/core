"""
Services for DTN 
"""

from core.misc.ipaddress import Ipv4Prefix
from core.service import CoreService


class IbrDtn(CoreService):
    """
    This will run the IBR Disruption Tolerant Network node
    """
    # a unique name is required, without spaces
    name = "IBR_DTN"
    # you can create your own group here
    group = "DTN"
    # list executables that this service requires
#    executables = ('/usr/local/bin/dtnd',)
    # list of other services this service depends on
    dependencies = ()
    # per-node directories
    dirs = ()
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    configs = ("dtnd.conf","dtnd-launch.sh",)
    # this controls the starting order vs other enabled services
    startindex = 50
    # list of startup commands, also may be generated during startup
    startup = ("bash dtnd-launch.sh",)
    # list of shutdown commands
    shutdown = ("pkill dtnd",)

    @classmethod
    def generate_config(cls, node, filename):
        if filename == cls.configs[0]:
            return cls.generate_dtnd_config(node)
        if filename == cls.configs[1]:
            return cls.generate_dtnd_launch(node)

    @classmethod
    def generate_dtnd_config(cls, node):
        """
        Simple dtnd config
        """
        cfg ="""
#####################################
# IBR-DTN daemon                    #
#####################################
# see https://github.com/ibrdtn/ibrdtn/blob/master/ibrdtn/daemon/etc/ibrdtnd.conf
#
# the local eid of the dtn node
# default is the hostname
#
#local_uri = dtn://node.dtn
#
# specifies an additional logfile
#
logfile = /var/log/ibrdtn.log
# limit the numbers of bundles in transit (default: 5)
limit_bundles_in_transit = 5000
# routing strategy
#
# values: default | epidemic | flooding | prophet | none
#
# In the "default" the daemon only delivers bundles to neighbors and static
# available nodes. The alternative module "epidemic" spread all bundles to
# all available neighbors. Flooding works like epidemic, but do not send the
# own summary vector to neighbors. Prophet forwards based on the probability
# to encounter other nodes (see RFC 6693).
#
routing = epidemic
#
# forward bundles to other nodes (yes/no)
#
routing_forwarding = yes



"""
        interfaces=" ".join([cls.ifc_name(ifc) for ifc in node.netifs()])
        cfg += "net_interfaces = %s\n"%interfaces
        for ifc in node.netifs():
            if hasattr(ifc, 'control') and ifc.control is True:
                continue
            cfg += "net_%s_type = tcp\n"%ifc.name
            cfg += "net_%s_interface = %s\n"%(ifc.name, ifc.name)
            cfg += "net_%s_port = 4556\n"%ifc.name
        return cfg

    @classmethod
    def generate_dtnd_launch(cls, node):
        """
        Simple gateway config
        """
        cfg ="#!/bin/bash\n"
        cfg += "sleep 1\n"
        cfg += "echo $$ > dtnd-launch.pid\n"
        cfg += "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib\n"
        cfg += "dtnd -c dtnd.conf >> dtnd.log 2>&1\n"

        return cfg

    @staticmethod
    def ifc_name(x):
        """
        Generate a subnet declaration block given an IPv4 prefix string
        for inclusion in the config file.
        """
        if hasattr(x, 'control') and x.control is True:
            return ""
        return x.name
    
class DtnTunnel(CoreService):
    """
    This will create a DTN based IP tunnel
    """
    # a unique name is required, without spaces
    name = "DTN_Tunnel"
    # you can create your own group here
    group = "DTN"
    # list executables that this service requires
#    executables = ('/usr/local/bin/dtnd',)
    # list of other services this service depends on
    dependencies = ()
    # per-node directories
    dirs = ()
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    configs = ("dtntunnel.conf","dtntunnel-launch.sh",)
    # this controls the starting order vs other enabled services
    startindex = 56
    # list of startup commands, also may be generated during startup
    startup = ("bash dtntunnel-launch.sh",)
    # list of shutdown commands
    shutdown = ("pkill dtntunnel",)

    @classmethod
    def generate_config(cls, node, filename):
        if filename == cls.configs[0]:
            return cls.generate_dtntunnel_config(node)
        if filename == cls.configs[1]:
            return cls.generate_dtntunnel_launch(node)

    @classmethod
    def generate_dtntunnel_config(cls, node):
        """
        Simple dtntunnel config
        """
        cfg ="""
# The IP can be any of your choosing, should be in the same subnet on the other end of the tunnel
IP=192.168.1.n/24
# The target node needs to be known on the dtn network, the "tunnel" bit can vary
TARGET=dtn://node/tunnel
# one hour should be enough, as long as we don't run out of data
LIFETIME=3600
"""
        return cfg

    @classmethod
    def generate_dtntunnel_launch(cls, node):
        """
        Set up the DTN tunnel
        """
        cfg ="#!/bin/bash\n"
        cfg += "echo $$ > dtntunnel-launch.pid\n"
        cfg += "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib\n"
        cfg += "source dtntunnel.conf\n"
        cfg += "dtntunnel -d dtn0 -l $LIFETIME -D $TARGET\n"
        cfg += "ip addr add $IP dev dtn0\n"
        cfg += "ip link set dev dtn0 up\n"
        
        return cfg
    
class DtnSink(CoreService):
    """
    This will create a DTN sink for messages
    """
    # a unique name is required, without spaces
    name = "DTN_Sink"
    # you can create your own group here
    group = "DTN"
    # list executables that this service requires
#    executables = ('/usr/local/bin/dtnd',)
    # list of other services this service depends on
    dependencies = ()
    # per-node directories
    dirs = ()
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    configs = ("dtnsink.conf","dtnsink.sh",)
    # this controls the starting order vs other enabled services
    startindex = 56
    # list of startup commands, also may be generated during startup
    startup = ("dtntrigger mqtt dtnsink.sh",)
    # list of shutdown commands
    shutdown = ("pkill dtntrigger",)

    @classmethod
    def generate_config(cls, node, filename):
        if filename == cls.configs[0]:
            return cls.generate_dtnsink_config(node)
        if filename == cls.configs[1]:
            return cls.generate_dtnsink_launch(node)

    @classmethod
    def generate_dtnsink_config(cls, node):
        """
        Simple dtnsink config
        """
        cfg ="""
# pipe to sink the data into
PIPE=dtnpipe
"""
        return cfg

    @classmethod
    def generate_dtnsink_launch(cls, node):
        """
        Set up the DTN sink
        """
        cfg = """#!/bin/bash
#
# mqtt helper script to be called from dtntrigger
# writes the data to a named pipe for pulling into a
# mqtt listener
#
source dtnsink.conf

if [[ ! -p $PIPE ]]; then
    mkfifo $PIPE
fi

while IFS='' read -r payload || [[ -n "$payload" ]]; do
    echo "{\"source\":\"${B_SOURCE}\", \"timestamp\":\"${B_TIMESTAMP}\", \"sequencenumber\":\"${B_SEQUENCENUMBER}\", \"payload\":\"${payload}\"}"  >> $PIPE
done
"""
        return cfg
    
