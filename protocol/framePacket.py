from csv import writer

from protocol.packet import Packet
from core.binaryWriter import BinaryWriter
from core.binaryReader import BinaryReader

class FramePacket(Packet):
    def __init__(self):
        super().__init__()

    def decode(self, reader:BinaryReader):
        self.length = reader.readU32()
        self.packetData = reader.readBytes(self.length)

    def encode(self, writer:BinaryWriter, packetData):
        self.length = len(packetData)
        writer.writeU32(self.length)
        writer.writeBytes(packetData)