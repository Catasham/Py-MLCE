from protocol.packet import Packet
from core.binaryReader import BinaryReader
from core.binaryWriter import BinaryWriter

class LoginPacket(Packet):
    def __init__(self):
        super().__init__("login")

    def encode(self, writer:BinaryWriter, seed=0, dimension=0, mapHeight=0, maxPlayers=10):
        # testing
        #a = "01000000000000000700640065006600610075006c007402c2c44be6f17b5700000000000064000000000000000000000000000000000000000000010000000000000000000000000000010000180001400806ffffff5800000040000000e8ca003d4ccccd3dcccccd100000fa000c004d0043007c0046006f0072006b00480065006c006c006f000004000000000e97e1e4000000000028efda460200a600ffffffed00000024"
        #b = bytearray.fromhex(a)
        #writer.writeBytes(b)
        #return
        
        super().encode(writer)
        writer.writeU32(0)
        writer.writeStringUtf16("")
        writer.writeStringUtf16("default")
        writer.writeI64(seed) # Seed
        writer.writeU32(0) # Gamemode
        writer.writeU8(0) # Dimension
        writer.writeU8(0) # Mapheight
        writer.writeU8(10) # Max players
        writer.writeU64(0) # Offline Xuid
        writer.writeU64(0) # Online Xuid
        writer.writeBool(0) # Friends only
        writer.writeU32(0) # UGC players version
        writer.writeU8(0) # Difficulty
        writer.writeU32(0) # Multiplayer instance id
        writer.writeU8(0) # Player index
        writer.writeU32(0) # Skin ID
        writer.writeU32(0) # Cape ID
        writer.writeBool(0) # Is guest
        writer.writeBool(0) # New sea level
        writer.writeU32(0) # Game priveledges
        writer.writeU16(0) # XZ size
        writer.writeU8(8) # Hellscale

        return
        writer.writeU32(0)
        writer.writeStringUtf16("")
        writer.writeStringUtf16("default")
        writer.writeU64(seed) # Seed
        writer.writeU8(0) # Gamemode
        writer.writeU8(dimension) # Dimension
        writer.writeU8(mapHeight)
        writer.writeU8(maxPlayers)
        writer.writeU64(0)
        writer.writeU64(0)
        writer.writeU32(0)
        writer.writeU8(0)
        writer.writeU32(0) # Skin id
        writer.writeU32(0)
        writer.writeBool(False)
        writer.writeBool(False)
        writer.writeU32(0xffffffed)
        writer.writeBytes(b"\x00\x00\x00")
        writer.writeU8(24)

    def decode(self, reader:BinaryReader):
        super().decode(reader)
        self.clientVersion = reader.readU32()
        self.username = reader.readUtf16()
        self.levelType = reader.readUtf16()
        self.seed = reader.readI64()
        self.gameType = reader.readU32()
        self.dimension = reader.readU8()
        self.mapHeight = reader.readU8()
        self.maxPlayers = reader.readU8()
        self.offlineXuid = reader.readU64()
        self.onlineXuid = reader.readU64()
        self.friendsOnly = reader.readBool()
        self.ugcPlayersVersion = reader.readU32()
        self.difficulty = reader.readU8()
        self.multiplayerInstanceId = reader.readU32()
        self.playerIndex = reader.readU8()
        self.skinId = reader.readU32()
        self.capeId = reader.readU32()
        self.isGuest = reader.readBool()
        self.newSeaLevel = reader.readBool()
        self.gamePriviledges = reader.readU32()
        self.xzSize = reader.readU16()
        self.hellScale = reader.readU8()

    def __str__(self):
        return f"""{super().__str__()}
        clientVersion: {self.clientVersion }
        username: {self.username}
        levelType: {self.levelType}
        seed: {self.seed}
        gameType: {self.gameType}
        dimension: {self.dimension}
        mapHeight: {self.mapHeight}
        maxPlayers: {self.maxPlayers}
        offlineXuid: {self.offlineXuid}
        onlineXuid: {self.onlineXuid}
        friendsOnly: {self.friendsOnly}
        ugcPlayersVersion: {self.ugcPlayersVersion}
        difficulty: {self.difficulty}
        multiplayerInstanceId: {self.multiplayerInstanceId}
        playerIndex: {self.playerIndex}
        skinId: {self.skinId}
        capeId: {self.capeId}
        isGuest: {self.isGuest}
        newSeaLevel: {self.newSeaLevel}
        gamePriviledges: {self.gamePriviledges}
        xzSize: {self.xzSize}
        hellScale: {self.hellScale}
        """