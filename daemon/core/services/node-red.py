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
        cfg = """[{"id":"5a373772.6f6b98","type":"tab","label":"Flow 1","disabled":false,"info":""},{"id":"bac2efc.047b89","type":"mqtt-broker","z":"","name":"","broker":"localhost","port":"1883","clientid":"","usetls":false,"compatmode":false,"keepalive":"60","cleansession":true,"birthTopic":"","birthQos":"0","birthPayload":"","closeTopic":"","closeQos":"0","closePayload":"","willTopic":"","willQos":"0","willPayload":""},{"id":"c57e9724.5b45c8","type":"mqtt in","z":"5a373772.6f6b98","name":"","topic":"#","qos":"2","broker":"bac2efc.047b89","x":240,"y":260,"wires":[["d28d76c1.0c1628"]]},{"id":"d28d76c1.0c1628","type":"debug","z":"5a373772.6f6b98","name":"","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"false","x":510,"y":260,"wires":[]}]
"""
        return cfg

