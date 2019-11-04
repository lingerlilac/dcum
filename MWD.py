import random
from pox.core import core
import pox
log = core.getLogger()

from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.tcp import tcp
from pox.lib.packet.udp import udp
from pox.lib.packet.arp import arp
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.util import str_to_bool, dpid_to_str
from pox.lib.recoco import Timer

import pox.openflow.libopenflow_01 as of
from AppPort import TypeToDelayRequirements, PortToType

from pox.lib.revent import *
from Queue import *
import time
import sys

class myPacket(object):
    def __init__(self, msg, intime):
        self.msg = msg
        self.intime = intime

class Flow(object):
    def __init__(self, srcip, dstip, srcport, dstport):
        self.srcip = srcip
        self.dstip = dstip
        self.srcport = srcport
        self.dstport = dstport

class Qentry(object):
    def __init__(self, Qlen, SumDelay, AverDelay, DelayRequirement, Q):
        self.Qlen = Qlen
        self.SumDelay = SumDelay
        self.AverDelay = AverDelay
        self.DelayRequirement = DelayRequirement
        self.Q = Q
        self.time = time.time()

_TIMESLOT = 1
_PACKETS_PER_SLOT = 10
_OUT_PORT = of.OFPP_NORMAL

class MWscheduler(EventMixin):
    def __init__(self):
        self.TIMESLOT = _TIMESLOT
        self.listenTo(core)
        self.listenTo(core.openflow)
        
        self.queue = {}
        #self.l2ports = {}
        self.packetScheduled = 1
        self.totaldelay = 0
        self.packetSatisfied = 1
    
    def _scheduler(self):
        for dpid in self.queue:
            for port in self.queue[dpid]:
                for clientIP in self.queue[dpid][port]:
                    for flow in self.queue[dpid][port][clientIP]['flows']:
                        newTime = time.time()
                        self.queue[dpid][port][clientIP]['flows'][flow].SumDelay += self.queue[dpid][port][clientIP]['flows'][flow].Q.qsize() * (newTime - self.queue[dpid][port][clientIP]['flows'][flow].time)
                        self.queue[dpid][port][clientIP]['flows'][flow].AverDelay = self.queue[dpid][port][clientIP]['flows'][flow].SumDelay / self.queue[dpid][port][clientIP]['flows'][flow].Q.qsize()
                        self.queue[dpid][port][clientIP]['flows'][flow].time = newTime

    
        self.showQueue()
        for dpid in self.queue:
            for port in self.queue[dpid]:
                for clientIP in self.queue[dpid][port]:
                    for flow in self.queue[dpid][port][clientIP]['flows']:
                        Q = self.queue[dpid][port][clientIP]['flows'][flow].Q
                        while Q.empty() == False:
                            myPacket = Q.get()
                            core.openflow.sendToDPID(dpid, myPacket.msg)
                    for flow in self.queue[dpid][port][clientIP]['flows'].keys():
                        del self.queue[dpid][port][clientIP]['flows'][flow]
        #self.queue[dpid][port][clientIP]['l4ports'].remove(flow[3])

        return

        for dpid in self.queue:
            while nPackets != 0:
                flowSelected = None
                AverDelayMax = 0
                for flow in self.queue[dpid]:
                    if self.queue[dpid][flow].AverDelay > AverDelayMax:
                        AverDelayMax, flowSelected = self.queue[dpid][flow].AverDelay, flow
                if flowSelected == None:
                    break
                #print "Scheduling Flow:", flowSelected.srcip, flowSelected.dstip, flowSelected.srcport, flowSelected.dstport, self.queue[dpid][flowSelected].Q.qsize(), self.queue[dpid][flowSelected].AverDelay, self.queue[dpid][flowSelected].DelayRequirement
                while self.queue[dpid][flowSelected].Q.empty() == False and nPackets != 0:
                    nPackets -= 1
                    myPacket = self.queue[dpid][flowSelected].Q.get()
                    core.openflow.sendToDPID(dpid, myPacket.msg)
                    
                    
                    self.packetScheduled += 1
                    delay = time.time() - myPacket.intime
                    self.queue[dpid][flowSelected].SumDelay -= delay
                    self.totaldelay += delay
                    if delay < self.queue[dpid][flowSelected].DelayRequirement:
                        self.packetSatisfied += 1
                if self.queue[dpid][flowSelected].Q.empty():
                    del self.queue[dpid][flowSelected]
        #print "dpid:", dpid
        #print "average delay:", self.totaldelay / self.packetScheduled
#print "satisfied:", self.packetSatisfied * 100.0 / self.packetScheduled, "%"


        #print "packetcnt, totaldelay, averagedelay", self.packetScheduled, self.totaldelay, self.totaldelay/self.packetScheduled
        
    def showQueue(self):
        print "--------"
        for dpid in self.queue:
            print dpid
            for port in self.queue[dpid]:
                print '\t', port
                for clientIP in self.queue[dpid][port]:
                    print '\t\t', clientIP
                    #print '\t\t\t',
                    #for l4port in self.queue[dpid][port][clientIP]['l4ports']:
                    #    print l4port,
                    #print
    
                    for flow in self.queue[dpid][port][clientIP]['flows']:
                        print '\t\t\t', flow[0], flow[1], flow[2], flow[3]
                        print '\t\t\t', self.queue[dpid][port][clientIP]['flows'][flow].Q.qsize(), self.queue[dpid][port][clientIP]['flows'][flow].AverDelay
        print "--------"
    
    def send_packet_out_directly(self, event):
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        port = _OUT_PORT
        msg.actions.append(of.ofp_action_output(port = port))
        event.connection.send(msg)
    
    def add_flow_entry(self, event):
        packet = event.parsed
        actions = []
        actions.append(of.ofp_action_output(port = _OUT_PORT))
        match = of.ofp_match.from_packet(packet, event.port)
        msg = of.ofp_flow_mod(command=of.OFPFC_ADD,
                              idle_timeout = 10,
                              hard_timeout=of.OFP_FLOW_PERMANENT,
                              buffer_id=event.ofp.buffer_id,
                              actions=actions,
                              match=match)
        event.connection.send(msg.pack())

    def _handle_ConnectionUp(self, event):
        dpid = event.connection.dpid
        self.queue[dpid] = {}
        for port in event.connection.features.ports:
            self.queue[dpid][port.port_no] = {}
        self._timer = Timer(self.TIMESLOT, self._scheduler, recurring=True)
        print "ConnectionUp:", dpid_to_str(event.connection.dpid)
    
    def _handle_PacketIn (self, event):
        '''
        for m in event.connection.features.ports:
            for k, v in vars(m).items():
                print '\t', k, v
        '''
        dpid = event.connection.dpid
        packet = event.parsed
        
        if isinstance(packet.next, ipv4):
            if isinstance(packet.next.next, udp) or isinstance(packet.next.next, tcp):
                srcip, dstip, srcport, dstport = packet.next.srcip, packet.next.dstip, packet.next.next.srcport, packet.next.next.dstport
                print srcip, dstip, srcport, dstport
                if srcip.in_network('192.168.0.0/16') and not srcip.in_network('192.168.0.0/24'):
                    if not srcip.in_network('192.168.0.0/24'):
                        l2port = event.port
                        if srcip not in self.queue[dpid][l2port]:
                            self.queue[dpid][l2port][srcip] = {'l4ports' : set(), 'flows': {}}
                        if srcport not in self.queue[dpid][l2port][srcip]['l4ports']:
                            self.queue[dpid][l2port][srcip]['l4ports'].add(srcport)
                        print 'building', srcip, dstip, srcport, dstport
                    self.add_flow_entry(event)
                    #self.send_packet_out_directly(event)
                    
                    return
                
                flow = (srcip, dstip, srcport, dstport)
                outport = _OUT_PORT
                clientIP = None
                for l2port in self.queue[dpid]:
                    for ip in self.queue[dpid][l2port]:
                        if dstport in self.queue[dpid][l2port][ip]['l4ports']:
                            outport = l2port
                            clientIP = ip



                if outport == _OUT_PORT:
                    self.send_packet_out_directly(event)
                    return
                
                
                appType = "default"
                if srcport in PortToType:
                    appType = PortToType[srcport]
                if flow not in self.queue[dpid][outport][clientIP]['flows']:
                    self.queue[dpid][outport][clientIP]['flows'][flow] = Qentry(0, 0, 0, TypeToDelayRequirements[appType], Queue())
                        #print 'enqueue', srcip, dstip, srcport, dstport
                msg = of.ofp_packet_out()
                msg.data = event.ofp
                msg.actions.append(of.ofp_action_output(port = _OUT_PORT))
                self.queue[dpid][outport][clientIP]['flows'][flow].Q.put(myPacket(msg, time.time()))
        
        else:
            #print "Sending packet(not IP)"

            self.add_flow_entry(event)

def launch ():
    core.registerNew(MWscheduler)

