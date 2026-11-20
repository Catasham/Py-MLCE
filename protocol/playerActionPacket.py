from protocol.packet import Packet
from core.binaryReader import BinaryReader

class PlayerActionPacket(Packet):
    def __init__(self):
        super().__init__("playerActionPacket")

    def decode(self, reader:BinaryReader):
        super().decode(reader)
        self.action = reader.readU8()
        self.x = reader.readI32()
        self.y = reader.readU8()
        self.z = reader.readI32()
        self.face = reader.readU8()