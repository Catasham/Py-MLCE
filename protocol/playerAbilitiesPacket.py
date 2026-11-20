from protocol.packet import Packet
from core.binaryWriter import BinaryWriter
from core.binaryReader import BinaryReader

class PlayerAbilitiesPacket(Packet):

    def __init__(self):
        super().__init__("setCarriedItem")

    def encode(self, writer:BinaryWriter, flags=0, flySpeed:float=1.0, walkSpeed:float=1.0):
        super().encode(writer)
        self.flags = flags
        self.flySpeed = flySpeed
        self.walkSpeed = walkSpeed

        writer.writeU8(self.flags)
        writer.writeFloat(self.flySpeed)
        writer.writeFloat(self.walkSpeed)

    def decode(self, reader:BinaryReader):
        self.flags = reader.readU8()
        self.flySpeed = reader.readFloat()
        self.walkSpeed = reader.readFloat()

    def __str__(self):
        return f"""{super().__str__()}
        flags: {self.flags}
        flySpeed: {self.flySpeed}
        walkSpeed: {self.walkSpeed}
        """
