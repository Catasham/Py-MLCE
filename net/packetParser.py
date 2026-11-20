from core.binaryReader import BinaryReader
from core.binaryWriter import BinaryWriter

from protocol.packet import PacketId
from protocol.preLoginPacket import PreLoginPacket
from protocol.disconnectPacket import DisconnectReasonId, DisconnectPacket

class packetParser():
    def parsePreLogin(self, conn, data:bytearray):
        reader = BinaryReader(data)
        p = PreLoginPacket()
        p.decode(reader)
        self.playerName = p.playerName
        self.netcodeVersion = p.netcodeVersion

        print(f"Netcode version: {self.netcodeVersion}")
        print(f"Player name: {self.playerName}")
        #self._blockConnection()

        conn.sendAll()