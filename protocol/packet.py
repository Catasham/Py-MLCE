from abc import abstractmethod, ABC
from enum import IntEnum
from core.binaryWriter import BinaryWriter
from core.binaryReader import BinaryReader

MAGIC = 0x4D434C4E # uint32

class PacketId(IntEnum):
    keepAlive = 0
    login = 1
    preLogin = 2
    chat = 3
    setTime = 4

    setSpawnPosition = 6
    playerAction = 14
    setCarriedItem = 16
    playerAbilities = 202
    setObjective = 206
    disconnect = 255

class Packet(ABC):
    def __init__(self, packetName):
        self.packetName = packetName
        self.id = PacketId[self.packetName].value
        self.buffer = bytearray()

    @abstractmethod
    def encode(self, writer:BinaryWriter): writer.writeI8(self.id)

    @abstractmethod
    def decode(self, reader:BinaryReader): pass

    def __str__(self):
        return f"""{self.packetName}Packet
        packetId: {self.id}"""
