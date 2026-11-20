from protocol.packet import Packet
from core.binaryWriter import BinaryWriter
from core.binaryReader import BinaryReader

class SetObjectivePacket(Packet):

    def __init__(self):
        super().__init__("setObjective")

    def encode(self, writer:BinaryWriter, name:str, displayName:str, method:int):
        super().encode(writer)
        self.name = name
        self.displayName = displayName
        self.method = method

        writer.writeStringUtf16(self.name)
        writer.writeStringUtf16(self.displayName)
        writer.writeU8(self.method)

    def decode(self, reader:BinaryReader):
        self.slot = reader.readU16()

    def __str__(self):
        return f"""{super().__str__()}
        slot: {self.slot}
        """
