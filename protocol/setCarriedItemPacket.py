from protocol.packet import Packet
from core.binaryWriter import BinaryWriter
from core.binaryReader import BinaryReader

class SetCarriedItemPacket(Packet):

    def __init__(self):
        super().__init__("setCarriedItem")

    def encode(self, writer:BinaryWriter, slot:int=1):
        super().encode(writer)
        self.slot = slot

        writer.writeU16(self.slot)

    def decode(self, reader:BinaryReader):
        self.slot = reader.readU16()

    def __str__(self):
        return f"""{super().__str__()}
        slot: {self.slot}
        """
