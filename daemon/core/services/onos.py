"""
Create an ONOS service
"""

from core.misc.ipaddress import Ipv4Prefix
from core.service import CoreService
from core.service import ServiceManager


class ONOS(CoreService):
    """
    This is a sample user-defined service.
    """
    # a unique name is required, without spaces
    name = "ONOS"
    # you can create your own group here
    group = "SDN"
    # list of other services this service depends on
    dependencies = ('OvsService',)
    # per-node directories
    dirs = ()
    # generated files (without a full path this file goes in the node's dir,
    #  e.g. /tmp/pycore.12345/n1.conf/)
    configs = ('onos.conf','onos-dynamic.conf','onos.sh','onosapps.py')
#    # this controls the starting order vs other enabled services
#    _startindex = 50
    # list of startup commands, also may be generated during startup
    startup = ('bash onos.sh',)
    # list of shutdown commands
    shutdown = ()

    @classmethod
    def generate_config(cls, node, filename):
        if filename == cls.configs[0]:
            return cls.generateOnosConf(node)
        elif filename == cls.configs[1]:
            return cls.generateOnosDynamic(node)
        elif filename == cls.configs[2]:
            return cls.generateOnosBoot(node)
        elif filename == cls.configs[3]:
            return cls.generateOnosApps(node)
        else:
            raise ValueError("file name (%s) is not a known configuration: %s",
                             filename, cls.configs)


    @classmethod
    def generateOnosApps(cls, node):
        """
        creates a python script to bootstrap the onos service
        """
        cfg ="""
import ConfigParser
import argparse
import sys
import json
import time
import requests

user = ''
password = ''

def main():
    parser = argparse.ArgumentParser(description='Initialise ONOS instance')
    parser.add_argument('--config',
                        '-c',
                        nargs='+',
                        default='onos.conf',
                        metavar='file',
                        help='an ini-style file containing configuration options')

    parser.add_argument('--dynamic',
                        '-d',
                        nargs='+',
                        default='onos-dynamic.conf',
                        metavar='file',
                        help='an ini-style file containing dynamic configuration options (dpidmap and portmap)')

    args = parser.parse_args()

    config = ConfigParser.SafeConfigParser()
    config.read(args.config)

    dynamics = ConfigParser.SafeConfigParser()
    dynamics.read(args.dynamic)

    if not config.has_option('global', 'SERVERS'):
        print 'global section in config file must define a list of IP addresses of servers in the SERVERS option'
        sys.exit()

    if not config.has_option('global', 'USER'):
        print 'global section in config file must define an onos login username in the USER option'
        sys.exit()

    if not config.has_option('global', 'PASS'):
        print 'global section in config file must define an onos login password in the PASS option'
        sys.exit()

    if not config.has_option('global', 'APPLICATIONS'):
        print 'global section in config file must define a comma-separated list of applications in the APPLICATIONS option'
        sys.exit()

    global user, password
    user = config.get('global', 'USER')
    password = config.get('global', 'PASS')

    desiredapps = config.get('global', 'APPLICATIONS').split(',')
    servers = config.get('global', 'SERVERS').split(',')
    dpidmap = dict(dynamics.items('dpidmap'))
    d_portmap = load_portmap(dynamics, dpidmap)
    
    (clusterconfig, clusterindex) = init_cluster_data(config)
    start_applications(servers, desiredapps)
    start_clusters(servers, clusterconfig, clusterindex)
    # sleep because onos will probably crash after cluster init
    time.sleep(5)
    set_friendly_names(servers, dpidmap)
    d_ports = gather_port_settings(d_portmap,servers)
    set_network_conf(servers,'ports', d_ports)
    d_rr_conf = create_routing_config(d_portmap, servers)
    set_network_conf(servers,'apps', d_rr_conf)

def load_portmap(config, d_dpidmap):
    d_portmap = {}
    for node in d_dpidmap:
        key = 'of:'+d_dpidmap[node]
        if config.has_section(node+'_portmap'):
            d_portmap[key]={}
            d_ports = dict(config.items(node+'_portmap'))
            for port in d_ports:
                l_values = d_ports[port].replace('(','').replace(')','').split(',')
                d_portmap[key][port]={'mac':expand_mac(l_values[0]),
                                       'ip':l_values[1]}
    return d_portmap

def create_routing_config(d_portmap, l_servers):
    l_prefix = []
    firstmac=''
    for device in d_portmap:
        for interface in d_portmap[device]:
            mac = d_portmap[device][interface]['mac']
            doc = {'ipPrefix' : calculate_prefix(d_portmap[device][interface]['ip']),
                   'type' : 'PUBLIC',
                   'gatewayIp' : strip_subnet(d_portmap[device][interface]['ip'])}
            if doc not in l_prefix:
                l_prefix.append(doc)
                firstmac=mac

    d_conf = {'org.onosproject.reactive.routing':
              {'reactiveRouting':
               {'ip4LocalPrefixes':l_prefix,
                'virtualGatewayMacAddress':firstmac}}}
    return d_conf

def expand_mac(mac):
    parts = list(mac)
    expanded=''
    i=0
    while i<len(parts):
        if i>0 and i%2==0:
            expanded += ':'
        expanded += parts[i]
        i += 1
    return expanded
            
def strip_subnet(ip):
    return ip.split('/')[0]

def calculate_prefix(ip):
    (addr, subnet) = ip.split('/')
    #to-do, actually do this properly
    parts = addr.split('.')
    return parts[0]+'.'+parts[1]+'.'+parts[2]+'.0/'+subnet
    
def set_network_conf(l_servers, key, data):
    for server in l_servers:
        url = 'http://'+server+':8181/onos/v1/network/configuration/'+key
        p = requests.post(url, auth=(user,password), data=json.dumps(data));
        if 201 == p.status_code or 200 == p.status_code:
            print 'set '+key+' network conf on '+server
        else:
            print 'unable to set '+key+' network conf: '+str(p.status_code)+': '+p.text
        

def gather_port_settings(d_portmap, l_servers):
    for server in l_servers:
        wait_for_server(server)
        d_ports = {}
        devices = {}
        url = 'http://'+server+':8181/onos/v1/devices'
        while len(devices) < 1:
            r = requests.get(url, auth=(user,password), headers={'Accept':'application/json'})
            devices = r.json()
        print "Loaded info about %d devices" % len(devices)
        # So now we know all the devices connected to this server
        # loop over it to discover all the ports that form part of it
        for device in devices['devices']:
            d_url = url + '/' + device['id'] + '/ports'
            d_device_ports = {}
            while len(d_device_ports) < 1:
                r2 = requests.get(d_url, auth=(user,password), headers={'Accept':'application/json'})
                d_device_ports = r2.json()
            print "Loaded info about %d ports" % len(d_device_ports)
                
            for port in d_device_ports['ports']:
                if port['port'] == 'local':
                    continue
                mac = port['annotations']['portMac']
                iface = port['annotations']['portName']
#                print 'Checking config for '+iface+'/'+mac
                if not device['id'] in d_portmap:
                    continue
                d_device = d_portmap[device['id']]
                if not iface in d_device:
                    continue
                port_id=str(device['id'] + '/' + port['port'])
                d_ports[port_id]={'interfaces':[]}
                ip = d_device[iface]['ip']
                #overwrite mac
                mac = d_device[iface]['mac']
                d_ports[port_id]['interfaces'].append({'ips':[ip],'mac':mac})
        return d_ports

def wait_for_server(server):
    url = 'http://'+server+':8181/onos/v1/system'
    while True:
        try:
            r = requests.get(url, auth=(user,password))
            if 200 == r.status_code:
                break
            else:
                print server+' is not up, waiting 5 seconds and trying again'
                time.sleep(5)
        except requests.exceptions.ConnectionError:
            print server+' is not up, waiting 5 seconds and trying again'
            time.sleep(5)


def init_cluster_data(config):
    clusters = config.get('global', 'CLUSTERS').split(',')
    clusterconfig = {}
    clusterindex = {}
    for cluster in clusters:
        if not cluster:
            break
        members = config.get(cluster, 'members').split(',')
        clusterconfig[cluster] = {}
        clusterconfig[cluster]['nodes'] = []
        for member in members:
            clusterconfig[cluster]['nodes'].append({'ip':member})
            if member in clusterindex:
                clusterindex[member].append(cluster)
            else:
                clusterindex[member] = [cluster]
        clusterconfig[cluster]['ipPrefix'] = config.get(cluster, 'ipPrefix')
    return (clusterconfig, clusterindex)

def start_applications(servers, desired):
    for server in servers:
        wait_for_server(server)
        url = 'http://'+server+':8181/onos/v1/applications'
        r = requests.get(url, auth=(user, password))
        onosappsjson = None
        if 200 == r.status_code:
            onosappsjson = r.json()
        else:
            raise ValueError('Failed to contact ONOS server at %s with username %s and password %s: %d', url, user, password, r.status_code)

        applicationindex = {}
        for application in onosappsjson['applications']:
            parts = application['name'].split('.')
            if parts[-1] in applicationindex:
                #uh-oh, duplicate shortname, use shortest path
                #            print 'duplicate shortname found '+application['name']+' and '+applicationindex[parts[-1]]
                if len(application['name']) < len(applicationindex[parts[-1]]):
                    #                print 'using '+application['name']
                    applicationindex[parts[-1]] = application['name']
            else:
                applicationindex[parts[-1]] = application['name']

        # now we know which applications are available and their 'short' names
        fullnames = []
        for application in desired:
            if application in applicationindex:
                fullnames.append(applicationindex[application])

        # now ask ONOS to load them
        for application in fullnames:
            print 'Activating '+application
            retry = 10
            success = False
            while retry > 0:
                p = requests.post(url+'/'+application+'/active', auth=(user, password))
                if 201 == p.status_code or 200 == p.status_code:
                    success = True
                    break
                else:
                    print 'Got status code '+str(p.status_code)+', retrying...'
                    retry -= 1
            if not success:
                print 'Failed to activate '+application

def start_clusters(servers, clusterconfig, clusterindex):
    # Now cluster the servers together
    for server in servers:
        url = 'http://'+server+':8181/onos/v1/cluster/configuration'
        if not server in clusterindex:
            break
        # generate cluster configuration for any clusters that this server is a member of
        for cluster in clusterindex[server]:
            cconf = clusterconfig[cluster]
            p = requests.post(url, auth=(user, password), data=json.dumps(cconf))
            if 201 == p.status_code or 200 == p.status_code:
                print 'Added '+server+' to cluster '+cluster
                success = True
                break
            else:
                print 'unable to form cluster: '+str(p.status_code)+':'+p.text

def set_friendly_names(servers, dpidmap):
    for server in servers:
        wait_for_server(server)
        # Now give some more friendly names
        for name in dpidmap:
            uri = 'of:'+dpidmap[name]
            message = {}
            message['name'] = name
            url = 'http://'+server+':8181/onos/v1/network/configuration/devices/'+uri+'/basic'
            p = requests.post(url, auth=(user, password), data=json.dumps(message))


if __name__ == "__main__":
    main()

"""
        return cfg
        
    @classmethod
    def generateOnosBoot(cls, node):
        """
        Returns a shell script that starts ONOS
        """
        cfg = "#!/bin/sh\n"
        cfg += "# auto-generated by ONOS (onos.py)\n"

        for ifc in node.netifs():
#            cfg += 'echo "Node %s has interface %s"\n' % (node.name, ifc.name)
            # here we do something interesting
#            cfg += "\n".join(map(cls.subnetentry, ifc.addrlist))
#            cfg += 'echo "\tMAC:%s"\n' % str(ifc.hwaddr)
            if hasattr(ifc, 'control') and ifc.control is True:
                continue
            cfg += "\n".join([cls.subnetdelete(ifc.name,x) for x in ifc.addrlist])
        netif1 = next(node.netifs())

        cfg += "\n"
            
        cfg += "# Get the right Java\n"
        cfg += "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/\n"
        cfg += "LOGDIR=$PWD\n"
        cfg += "export ONOS_ROOT=$PWD/onos\n"
        cfg += "mkdir $ONOS_ROOT\n"
        cfg += "cd $ONOS_ROOT\n"
        cfg += "tar zxf /tmp/onos.tar.gz --strip 1\n"
        cfg += "\n"
        cfg += "DPID=%0.4X%s\n" % (node.objid, str(netif1.hwaddr).replace(':',''))
        cfg += "ovs-vsctl set Bridge ovsbr0 other_config:datapath-id=$DPID\n"
        cfg += "bin/onos-service server >> $LOGDIR/onos.log 2>&1 &\n\n"

        cfg+= "# Start up onos applications, loop till ONOS is up.\n"
        cfg+= "while true\n"
        cfg+= "do\n"
        cfg+= " SC=$(curl -I -u onos:rocks -o /dev/null -w '%{http_code}' http://localhost:8181/onos/v1/applications)\n"
        cfg+= " if [ $SC -eq 200 ]; then break\n"
        cfg+= " fi\n"
        cfg+= " sleep 5\n"
        cfg+= "done\n"
        cfg+= "python $LOGDIR/onosapps.py -c $LOGDIR/onos.conf -d $LOGDIR/onos-dynamic.conf >> $LOGDIR/onos.log 2>&1\n"

        
        return cfg

    @classmethod
    def generateOnosConf(cls, node):
        """
        Returns a configuration script for ONOS
        """
        cfg = "# auto-generated by ONOS (onos.py)\n\n"
        cfg += "[global]\n"
        cfg += "APPLICATIONS=openflow,fwd,proxyarp\n"
        cfg += "SERVERS=localhost\n"
        cfg += "USER=onos\n"
        cfg += "PASS=rocks\n"
        cfg += "CLUSTERS=\n"
        cfg += "\n"
        cfg += "[examplecluster1]\n"
        cfg += "members=ip1,ip2\n"
        cfg += "ipPrefix=10.0.0.*\n"
        return cfg

    @classmethod
    def generateOnosDynamic(cls, node):
        """
        Returns a dynamic configuration script that needs to be rewritte on each experiment
        """
        cfg = "# auto-generated by ONOS (onos.py), please don't modify\n\n"
        cfg += "[dpidmap]\n"
        netif1 = next(node.netifs())
        #dpid address, top 16 bits are vendor defined, for openvswitch assume 0000
        cfg += "%s=%0.4X%s\n" % (node.name, node.objid, str(netif1.hwaddr).replace(':',''))
#        cfg += node.name+'=0000'+str(netif1.hwaddr).replace(':','')+'\n'
        cfg += "\n"
        cfg += "["+node.name+"_portmap]\n"
        # map from mac address to ip address
        for ifc in node.netifs():
            if hasattr(ifc, 'control') and ifc.control is True:
                continue
            cfg += "".join([cls.eth_to_ip(ifc,x) for x in ifc.addrlist])
        cfg += "\n"
        return cfg
    
    @staticmethod
    def subnetentry(x):
        """
        Generate a subnet declaration block given an IPv4 prefix string
        for inclusion in the config file.
        """
        if x.find(":") >= 0:
            # this is an IPv6 address
            return ""
        else:
            net = Ipv4Prefix(x)
            return 'echo " %s on network %s"\n' % (x,net)

    @staticmethod
    def subnetdelete(ifc, x):
        """
        Generate a subnet deletion block given an IPv4 prefix string
        for inclusion in the config file.
        """
        return "ip addr del %s dev %s\n" %( x, ifc)

    @staticmethod
    def mac_to_ip(mac, x):
        """
        Generate a mac declaration block given an IPv4 prefix string
        for inclusion in the config file.
        """
        if x.find(":") >= 0:
            # this is an IPv6 address
            return ""
        else:
            return '%s=%s\n' % (mac,x)

    @staticmethod
    def eth_to_ip(iface, x):
        """
        Generate a device declaration block given an IPv4 prefix string
        for inclusion in the config file.
        """
        if x.find(":") >= 0:
            # this is an IPv6 address
            return ""
        else:
            return '%s=(%s,%s)\n' % (iface.name,str(iface.hwaddr).replace(':',''), x)
        

# this is needed to load desired services when being integrated into core, otherwise this is not needed
#def load_services():
#    # this line is required to add the above class to the list of available services
#    ServiceManager.add(ONOS)
