from frame_builders import FrameBuilder, EthernetFrameBuilder, ARPFrameBuilder
from frame_consumers import EthernetFrameConsumer, ARPFrameConsumer
from socket import socket, AF_PACKET, SOCK_RAW
from utils import hex2str

MAC_SOURCE      = '\x08\x00\x27\x50\x25\x5f'
MAC_BROADCAST   = '\xFF\xFF\xFF\xFF\xFF\xFF'
IP_SOURCE       = '\x01\x01\x01\x01'
IP_DEST         = '\xC0\xA8\x01\x21'

ethernet_frame_builder = EthernetFrameBuilder(MAC_SOURCE, MAC_BROADCAST, EthernetFrameBuilder.TYPE_ARP)
arp_frame_builder = ARPFrameBuilder(ARPFrameBuilder.ETHERNET, ARPFrameBuilder.INTER_NETWORK, FrameBuilder.MAC_LENGTH, FrameBuilder.IP_LENGTH)


s = socket(AF_PACKET, SOCK_RAW, SOCK_RAW)
s.bind(('eth0', SOCK_RAW))

print 'SENDING: %s' % hex2str(ethernet_frame_builder.build(arp_frame_builder.build_request(MAC_SOURCE, IP_SOURCE, IP_DEST)))
s.send(ethernet_frame_builder.build(arp_frame_builder.build_request(MAC_SOURCE, IP_SOURCE, IP_DEST)))

for x in xrange(10):
    ethernet_frame = EthernetFrameConsumer(s.recv(1024))

    if ethernet_frame.mac_dest == MAC_BROADCAST:
        print 'broadcast_todo'
        continue

    if ethernet_frame.mac_dest != MAC_SOURCE:
        print 'not_for_me'
        continue

    if ethernet_frame.protocol != EthernetFrameBuilder.TYPE_ARP:
        print 'invalid_protocol'
        continue

    arp_frame = ARPFrameConsumer(ethernet_frame.payload)

    if arp_frame.operation != ARPFrameBuilder.ETHERNET_REP:
        print 'not_a_reply'
        continue

    print hex2str(arp_frame.mac_source)

    # print arp_frame.htype == '\x00\x01'
    # print arp_frame.ptype == '\x08\x00'
    # print arp_frame.hlen == '\x06'
    # print arp_frame.plen == '\x04'
    # print arp_frame.operation == ARPFrameBuilder.ETHERNET_REP
    # print arp_frame.mac_source == MAC_SOURCE
    # print arp_frame.ip_source == IP_SOURCE
    # print arp_frame.mac_dest == MAC_BROADCAST
    # print arp_frame.ip_dest == IP_DEST
    break