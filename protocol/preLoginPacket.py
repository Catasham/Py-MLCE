from protocol.packet import Packet
from protocol.hostOptions import HostOptions
from core.binaryWriter import BinaryWriter
from core.binaryReader import BinaryReader

UNIQUE_SAVE_NAME_LENGTH = 14

class PreLoginPacket(Packet):
    """Packet 2. Same layout both ways.

    Client -> server: netcodeVersion and the player's name in loginKey, everything else zero.
    Server -> client: the fields below describe the game being joined.
    """
    def __init__(self):
        super().__init__("preLogin")
        self.netcodeVersion = 0 # must equal the client's (560), or it is disconnected
        self.loginKey = "" # player name from the client, "-" from the server
        self.friendsOnlyBits = 0 # bit i set = player i in playerUids only shares created content with friends
        self.ugcPlayersVersion = 0 # counter of changes to playerUids; the client echoes it in Login
        self.playerUids = [] # online XUIDs of the players already in the game
        self.uniqueSaveName = bytes(UNIQUE_SAVE_NAME_LENGTH) # world id, used by the client's "banned levels" list
        self.hostOptions = HostOptions() # the 32-bit serverSettings field
        self.hostIndex = 0 # index into playerUids of the host player
        self.texturePackId = 0 # 0 = default; a client without this pack asks the host for it

    @property
    def playerName(self) -> str:
        return self.loginKey

    def encode(self, writer:BinaryWriter, netcodeVersion, loginKey="-", friendsOnlyBits=0, ugcPlayersVersion=0, playerUids:list=None, uniqueSaveName:bytes=b"", hostOptions:HostOptions=None, hostIndex=0, texturePackId=0):
        super().encode(writer)
        self.netcodeVersion = netcodeVersion
        self.loginKey = loginKey
        self.friendsOnlyBits = friendsOnlyBits
        self.ugcPlayersVersion = ugcPlayersVersion
        self.playerUids = playerUids or []
        self.uniqueSaveName = uniqueSaveName[:UNIQUE_SAVE_NAME_LENGTH].ljust(UNIQUE_SAVE_NAME_LENGTH, b"\x00")
        self.hostOptions = hostOptions or HostOptions()
        self.hostIndex = hostIndex
        self.texturePackId = texturePackId

        writer.writeI16(self.netcodeVersion)
        writer.writeStringUtf16(self.loginKey)
        writer.writeU8(self.friendsOnlyBits)
        writer.writeI32(self.ugcPlayersVersion)
        writer.writeU8(len(self.playerUids))
        for uid in self.playerUids:
            writer.writeU64(uid)
        writer.writeBytes(self.uniqueSaveName)
        writer.writeU32(self.hostOptions.toInt())
        writer.writeU8(self.hostIndex)
        writer.writeU32(self.texturePackId)

    def decode(self, reader:BinaryReader):
        self.netcodeVersion = reader.readI16()
        self.loginKey = reader.readUtf16()
        self.friendsOnlyBits = reader.readU8()
        self.ugcPlayersVersion = reader.readI32()
        playerCount = reader.readU8()
        self.playerUids = [reader.readU64() for _ in range(playerCount)]
        self.uniqueSaveName = bytes(reader.readBytes(UNIQUE_SAVE_NAME_LENGTH))
        self.hostOptions = HostOptions.fromInt(reader.readU32())
        self.hostIndex = reader.readU8()
        self.texturePackId = reader.readU32()

    def __str__(self):
        return f"""{super().__str__()}
        netcodeVersion: {self.netcodeVersion}
        loginKey: {self.loginKey}
        friendsOnlyBits: {self.friendsOnlyBits}
        ugcPlayersVersion: {self.ugcPlayersVersion}
        playerUids: {[hex(uid) for uid in self.playerUids]}
        uniqueSaveName: {self.uniqueSaveName}
        hostOptions: {self.hostOptions}
        hostIndex: {self.hostIndex}
        texturePackId: {self.texturePackId}
        """
