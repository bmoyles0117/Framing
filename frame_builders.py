class FrameBuilder(object):
    MAC_LENGTH      = '\x06'
    IP_LENGTH       = '\x04'

    def build(self, payload = ''):
        return self._build(payload)

class EthernetFrameBuilder(FrameBuilder):
    TYPE_ARP        = '\x08\x06'

    def __init__(self, mac_source, mac_dest, ether_type):
        self.mac_source = mac_source
        self.mac_dest = mac_dest
        self.ether_type = ether_type

    def _build(self, payload):
        return ''.join([
            self.mac_dest,
            self.mac_source,
            self.ether_type
        ]) + payload

class ARPFrameBuilder(FrameBuilder):
    ETHERNET        = '\x00\x01'
    ETHERNET_REQ    = '\x00\x01'
    ETHERNET_REP    = '\x00\x02'
    INTER_NETWORK   = '\x08\x00'
    MAC_BROADCAST   = '\x00\x00\x00\x00\x00\x00'

    def __init__(self, htype, ptype, hlen, plen):
        self.htype = htype
        self.ptype = ptype
        self.hlen = hlen
        self.plen = plen
        self.current_payload = None

    def build_request(self, mac_source, ip_source, ip_dest):
        return self._build(self.build_frame(self.ETHERNET_REQ, mac_source, ip_source, self.MAC_BROADCAST, ip_dest))

    def build_reply(self, mac_source, ip_source, mac_dest, ip_dest):
        return self._build(self.build_frame(self.ETHERNET_REP, mac_source, ip_source, mac_dest, ip_dest))

    def build_frame(self, request_type, mac_source, ip_source, mac_dest, ip_dest):
        return ''.join([
            request_type,
            mac_source,
            ip_source,
            mac_dest,
            ip_dest
        ])

    def _build(self, payload):
        return ''.join([
            self.htype,
            self.ptype,
            self.hlen,
            self.plen
        ]) + payload