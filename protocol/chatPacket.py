from protocol.packet import Packet
from core.binaryWriter import BinaryWriter
from core.binaryReader import BinaryReader

class ChatPacket(Packet):

    def __init__(self):
        super().__init__("chat")

    def encode(self, writer:BinaryWriter, message:str="Hello world!", messageType:int=0):
        super().encode(writer)
        self.stringCount = 1
        self.message = message
        self.messageType = messageType

        writer.writeU16(self.messageType)
        writer.writeStringUtf16(self.message)

    def decode(self):
        pass

    def __str__(self):
        return f"""{super().__str__()}

        """
