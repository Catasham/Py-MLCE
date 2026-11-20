from protocol.packet import Packet
from core.binaryWriter import BinaryWriter
from core.binaryReader import BinaryReader

class SetTimePacket(Packet):

    def __init__(self):
        super().__init__("setTime")

    def encode(self, writer:BinaryWriter, gameTime:int=6000, dayTime:int=0):
        super().encode(writer)
        self.gameTime = gameTime
        self.dayTime = dayTime

        writer.writeI64(self.gameTime)
        writer.writeI64(self.dayTime)

    def decode(self, reader:BinaryReader):
        self.gameTime = reader.readI64()
        self.dayTime = reader.readI64()

    def __str__(self):
        return f"""{super().__str__()}
        gameTime: {self.gameTime}
        dayTime: {self.dayTime}
        """
