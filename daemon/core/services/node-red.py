"""
Run node-red
"""

from core.misc.ipaddress import Ipv4Prefix
from core.service import CoreService


class MyService(CoreService):
    """
    Service to launch a node-red instance
    """
    # a unique name is required, without spaces
    name = "Node-RED"
    # you can create your own group here
    group = "IoT"
    # list executables that this service requires
    executables = ('/usr/bin/node-red',)
    # list of other services this service depends on
    dependencies = ()
    # per-node directories
    dirs = ()
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    configs = ("node-red-flows.json",)
    # list of startup commands, also may be generated during startup
    startup = ("node-red -c node-red-flows.json",)
    # list of shutdown commands
    shutdown = ("pkill node-red",)

    @classmethod
    def generate_config(cls, node, filename):
        """
        Return a string that will be written to filename, or sent to the
        GUI for user customization.
        """
        cfg = """
"""
        return cfg

