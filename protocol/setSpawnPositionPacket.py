from protocol.packet import Packet
from core.binaryWriter import BinaryWriter
from core.binaryReader import BinaryReader

class SetSpawnPositionPacket(Packet):

    def __init__(self):
        super().__init__("setSpawnPosition")

    def encode(self, writer:BinaryWriter, x:int=0, y:int=100, z:int=0):
        super().encode(writer)
        self.x, self.y, self.z = x, y, z

        writer.writeI32(self.x)
        writer.writeI32(self.y)
        writer.writeI32(self.z)

    def decode(self, reader:BinaryReader):
        self.x = reader.readI32()
        self.y = reader.readI32()
        self.z = reader.readI32()

    def __str__(self):
        return f"""{super().__str__()}
        x: {self.x}
        y: {self.y}
        z: {self.z}
        """
