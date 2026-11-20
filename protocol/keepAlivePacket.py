from protocol.packet import Packet
from core.binaryWriter import BinaryWriter
from core.binaryReader import BinaryReader

class KeepAlivePacket(Packet):
    def __init__(self):
        super().__init__("keepAlive")

    def encode(self, writer:BinaryWriter, gameId=0):
        super().encode(writer)
        self.gameId = gameId
        writer.writeI32(gameId)

    def decode(self, reader:BinaryReader):
        self.gameId = reader.readI32()

    def __str__(self):
        return f"""{super().__str__()}
        gameId: {self.gameId}
        """