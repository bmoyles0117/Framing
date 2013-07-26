from struct import unpack

class FrameConsumer(object):
    unpack_strategy = {}

    def __init__(self, frame):
        for attr, slice_ in self.unpack_strategy.items():
            frame_slice = frame[slice_.start:slice_.stop]
            setattr(self, attr, unpack('!%ss' % (len(frame_slice), ), frame_slice)[0])

class EthernetFrameConsumer(FrameConsumer):
    unpack_strategy     = {
        'mac_dest'      : slice(0, 6),
        'mac_source'    : slice(6, 12),
        'protocol'      : slice(12, 14),
        'payload'       : slice(14, None)
    }

class ARPFrameConsumer(FrameConsumer):
    unpack_strategy     = {
        'htype'         : slice(0, 2),
        'ptype'         : slice(2, 4),
        'hlen'          : slice(4, 5),
        'plen'          : slice(5, 6),
        'operation'     : slice(6, 8),
        'mac_source'    : slice(8, 14),
        'ip_source'     : slice(14, 18),
        'mac_dest'      : slice(18, 24),
        'ip_dest'       : slice(24, 28)
    }