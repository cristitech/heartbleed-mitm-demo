#!/usr/bin/python3
from mininet.net import Mininet, Containernet
from mininet.node import Host, OVSBridge, Node, Controller, Docker, UserSwitch, OVSSwitch
from mininet.nodelib import NAT
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Intf
from subprocess import call
import subprocess

def myNetwork():
    net = Containernet(controller=Controller)

    info( '*** Adding controller\n' )
    net.addController(name='c0')

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSSwitch)
    s2 = net.addSwitch('s2', cls=OVSSwitch)

    info( '*** Add hosts\n')

    # Attacker host
    mn_args = {
        "network_mode": "none",
        "dimage": "cristitech/attacker",
        "dcmd": None,
        "ip": "192.168.16.108/24",
    }
    H1 = net.addDocker('attacker', **mn_args)
    
    # Victim host
    mn_args = {
        "network_mode": "none",
        "dimage": "cristitech/victim",
        #"dcmd": "./start_app.sh",
        "ip": "192.168.16.109/24",
    }
    H2 = net.addDocker('victim', **mn_args)

    # Vulnerable server
    mn_args = {
        "network_mode": "none",
        "dimage": "cristitech/docker-heartbleed",
        "dcmd": None,
        "ip": "192.168.17.110/24",
    }
    H3 = net.addDocker('server', **mn_args)

    #cristitech/docker-heartbleed

    info( '*** Add links\n')
    net.addLink( H1, s1 )
    net.addLink( H2, s1 )
    net.addLink( H3, s2 )

    info ('*** Add Internet access\n')
    mn_args = {
        "ip": "192.168.16.1/24",
    }
    nat = net.addHost( 'nat0', cls=NAT, inNamespace=False, subnet='192.168.16.0/24', **mn_args )
    # Connect the nat to the switch
    net.addLink( nat, s1 )

    mn_args = {
        "ip": "192.168.17.1/24"
    }
    nat2 = net.addHost('nat1', cls=NAT, inNamespace=False, subnet='192.168.17.0/24', **mn_args)
    net.addLink(nat2, s2)

    info( '*** Starting network\n')
    net.start()
    H1.cmd('ip r a default via 192.168.16.1')
    H2.cmd('ip r a default via 192.168.16.1')
    
    # shutdown eth0
    H3.cmd('ip link set eth0 down')
    # power on server-eth0
    H3.cmd('ip link set server-eth0 up')
    # set default route
    H3.cmd('ip r a default via 192.168.17.1')

    # set apache servername
    H3.cmd('echo "ServerName 192.168.17.110" >> /etc/apache2/apache2.conf')
    # restart apache
    H3.cmd('apache2ctl restart')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
