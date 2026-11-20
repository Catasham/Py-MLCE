from core.binaryReader import BinaryReader
from core.binaryWriter import BinaryWriter

from protocol.packet import Packet, PacketId
from protocol.keepAlivePacket import KeepAlivePacket
from protocol.preLoginPacket import PreLoginPacket
from protocol.loginPacket import LoginPacket

import struct

class PacketHandler():
    def __init__(self):
        self._reader = BinaryReader(bytearray())

    # Append stream of data to buffer
    def addToBuffer(self, b:bytearray):
        self._reader.addToBuffer(b)

    # Turn a stream of data into a packet class
    def _parsePacket(self):
        packetId = struct.unpack("B", self._reader.readBytes(1))[0]

        packet = None

        match packetId:
            case PacketId.keepAlive.value: packet = KeepAlivePacket()
            case PacketId.preLogin.value: packet = PreLoginPacket()
            case PacketId.login.value: packet = LoginPacket()
            case _:
                raise ValueError(f"Unkown packet ID: {packetId}")

        # decode and return packet
        packet.decode(self._reader)
        return packet