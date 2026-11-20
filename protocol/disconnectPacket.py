from enum import Enum

from protocol.packet import Packet
from core.binaryWriter import BinaryWriter
from core.binaryReader import BinaryReader

class DisconnectReasonId(Enum):
    none = 0
    quitting = 1
    closed = 2
    loginTooLong = 3
    illegalStance = 4
    illegalPosition = 5
    movedTooQuickly = 6
    noFlying = 7
    kicked = 8
    timeOut = 9
    overflow = 10
    endOfStream = 11
    serverFull = 12
    outdatedServer = 13
    outdatedClient = 14
    unexpectedPacket = 15
    connectionCreationFailed = 16
    noMultiplayerPriviledgesHost = 17
    noMultiplayerPrivilegesJoin = 18
    noUgcAllLocal = 19
    NoUgcSingleLocal = 20
    contentRestrictedAllLocal = 21
    contentRestrictedSingleLocal = 22
    noUgcRemote = 23
    noFriendsInGame = 24
    banned = 25
    notFriendsWithHost = 26
    NatMismatch = 27

class DisconnectPacket(Packet):
    def __init__(self):
        super().__init__("disconnect")

    def encode(self, writer:BinaryWriter, reason:int=0):
        writer.writeI32(reason)

    def decode(self, reader:BinaryReader):
        self.reason = reader.readI32()