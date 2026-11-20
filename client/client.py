import struct
from time import time

from server.serverProperties import ServerProperties
from core.binaryReader import BinaryReader
from core.binaryWriter import BinaryWriter
from protocol.packet import PacketId
from socket import socket
from protocol.framePacketHandler import FramePacketHandler
# Packets
from protocol.packet import Packet
from protocol.keepAlivePacket import KeepAlivePacket
from protocol.preLoginPacket import PreLoginPacket
from protocol.loginPacket import LoginPacket
from protocol.setSpawnPositionPacket import SetSpawnPositionPacket
from protocol.playerAbilitiesPacket import PlayerAbilitiesPacket
from protocol.chatPacket import ChatPacket
from protocol.disconnectPacket import DisconnectPacket
from protocol.setTimePacket import SetTimePacket
from protocol.hostOptions import HostOptions

NETCODE_VERSION = 560
UGC_PLAYERS_VERSION = 0 # Counter of changes to the player list, not the protocol version (78 is Login's)

class Client:
    def __init__(self, connection:socket, serverProperties:ServerProperties):
        self._recvBuffer = BinaryWriter()
        self._serverProperties = serverProperties
        self._connection = connection
        self._framePacketHandler = FramePacketHandler()
        self.lastKeepAlive = time()
        self._maxTimeout = 60 # Max timeout time in seconds
         # Change the following
        self._loginKey = "-"
        self._friendsOnlyBits = 0
        self._playerCount = 0
        self._playerUids = []
        self._uniqueSaveName = b"world"
        self._serverSettings = HostOptions()
        self._hostIndex = 0
        self._texturePackId = 0
        self._playerName = ""
        self.connected = False

    def connect(self):
        print("Handling connection")
        packetReader = self._framePacketHandler.readPacketsFromFrame()

        # This byte is sent to start the connection
        self._connection.sendall(b"\x04")
        self._connecting = True

        while self._connecting:
            data = bytearray(self._connection.recv(1600))
            print(f"recv: {data}")

            # Add data to frame handler
            self._framePacketHandler.addToBuffer(data)

            # Handle packets from stream until there are none left
            for packet in packetReader:
                if packet == None: break
                connectionCode = self._handleConnectionPacket(packet)

                # Exit loop once connection is complete
                if connectionCode:
                    self._connecting = False
                    break

        self.connected = True
        # Send world data
        return

    def _handleConnectionPacket(self, packet:Packet): # What action to take for each packet
        if not packet: return
        print(packet)
        match packet.id:
            case PacketId.keepAlive.value:
                pass
                #self._connection.close()
                #self._connecting = False
                #self._keepAlive()
                #self.lastKeepAlive = time()
            case PacketId.preLogin.value:
                self._handlePreLogin(packet)
            case PacketId.login.value:
                self._handleLogin(packet)
                self._handleWorldSetup()
            case _:
                pass

    def _handlePacket(self, packet:Packet): # Non connection packets (move to client)
        print(packet)
        match packet.id:
            case _:
                pass

    def _sendFrame(self, writer:BinaryWriter):
        # Length starts every frame packet
        frameBuffer = bytearray(struct.pack(">I", len(writer.buffer)))
        # Put buffer after length
        frameBuffer.extend(writer.buffer)
        print(f"send: {frameBuffer}")
        self._connection.sendall(frameBuffer)

    def _keepAlive(self):
        if time() - self.lastKeepAlive >= 1:
            print("Keeping aliveee")
            writer = BinaryWriter()
            keepAlivePacket = KeepAlivePacket()
            keepAlivePacket.encode(writer)
            self._sendFrame(writer)
        else: print("Too many keep alives!")

    def _handleLogin(self, parsedPacket:Packet):
        writer = BinaryWriter()
        serverPacket = LoginPacket()
        serverPacket.encode(writer)
        self._sendFrame(writer)

    def _handlePreLogin(self, parsedPacket:Packet):
        self.playerName = parsedPacket.playerName
        self.netcodeVersion = parsedPacket.netcodeVersion

        # Check to see if netcode version matches servers
        if self.netcodeVersion != NETCODE_VERSION:
            raise ValueError(f"Unsupported netcode version: {self.netcodeVersion}")

        # Send back a prelogin packet
        print("Sending prelogin packet")
        writer = BinaryWriter()
        serverPacket = PreLoginPacket()
        serverPacket.encode(
            writer,
            NETCODE_VERSION,
            loginKey=self._loginKey,
            friendsOnlyBits=self._friendsOnlyBits,
            ugcPlayersVersion=UGC_PLAYERS_VERSION,
            playerUids=self._playerUids,
            uniqueSaveName=self._uniqueSaveName,
            hostOptions=self._serverSettings,
            hostIndex=self._hostIndex,
            texturePackId=self._texturePackId,
            )

        self._sendFrame(writer)

    def _handleWorldSetup(self):
        writer = BinaryWriter()
        setupPackets = [SetSpawnPositionPacket(), PlayerAbilitiesPacket(), ChatPacket()]
        for p in setupPackets:
            p.encode(writer)
            
        self._sendFrame(writer)