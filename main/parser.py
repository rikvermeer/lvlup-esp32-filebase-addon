header = bytes([0x55, 0x00])
footer = bytes([0xAA])

class Message(object):
    # [header, msg_length, msg_type, body_length, body, crc, footer]
    bts = None
    def __init__(self, bts):
        self.bts = bts
    @property
    def header(self):
        return self.bts[0:2]
    @property
    def footer(self):
        return self.bts[-1:]
    @property
    def checksum(self):
        return self.bts[-2:-1][0] #implicit cast to int
    @property
    def length(self):
        return len(self.bts)
    @property
    def msg_length(self):
        return self.bts[2]
    @property
    def msg_type(self):
        return self.bts[3:5]
    @property
    def body_length(self):
        return self.bts[5]
    @property
    def body(self):
        return self.bts[6:-2]
    @property
    def isvalid(self):
        return Message.validate(self) 
    @classmethod
    def validate(cls, msg):
        return (sum(msg.msg_type) + msg.body_length + sum(msg.body)) % 256 == msg.checksum

class Parser(object):
    buffer = bytes()
    cmds = []
    callback = None
    
    def __init__(self, callback):
        self.callback = callback

    def append_chunk(self, chunk):
        from binascii import hexlify
        
        self.buffer = self.buffer + chunk
        self.buffer, self.cmds = Parser.parse(self.buffer, self.cmds)
        # Make async
        self.callback(self.cmds)
        self.cmds = []

    @classmethod
    def parse(cls, buffer, cmds=[]):
        # Partition buffer by header    
        partitions = buffer.partition(header)

        if len(partitions[1]) == 0:
            # No header found, return full buffer
            return (partitions[0], cmds)

        # A header was found
        # partitions[0] is garbage, partitions[1] is our header
        # Find footer in partitions[2]
        tail = partitions[2].partition(footer)
        if len(tail[1]) == 0:
            # No footer found, partitions[2] is our return buffer
            # No commands are found
            return (header + partitions[2], cmds)

        # A footer was found
        # Add tail[0] to the found commands
        cmd = Message(bytes(header) + tail[0] + bytes(footer))
        cmds.append(cmd)

        if(len(tail[2]) > 0):
            #Recursivly parse tail[2]
            remainder, cmds = Parser.parse(tail[2], cmds)
            return (remainder, cmds)
        else:
            return (bytes(), cmds)
