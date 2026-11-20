from dataclasses import dataclass, fields
from enum import IntEnum

# The 32-bit "serverSettings" field of the pre-login packet.
# Bit layout from GAME_HOST_OPTION_BITMASK_* in Minecraft.Client/Common/App_Defines.h

class Difficulty(IntEnum):
    peaceful = 0
    easy = 1
    normal = 2
    hard = 3

class GameType(IntEnum):
    survival = 0
    creative = 1
    adventure = 2

class WorldSize(IntEnum):
    unset = 0
    classic = 1 # 54 chunks across
    small = 2 # 64 chunks across
    medium = 3 # 192 chunks across
    large = 4 # 320 chunks across

# name -> (bit shift, bit count)
_LAYOUT = {
    "difficulty": (0, 2),
    "friendsOfFriends": (2, 1),
    "gamertags": (3, 1),
    "gameType": (4, 2),
    "flatWorld": (6, 1),
    "structures": (7, 1),
    "bonusChest": (8, 1),
    "hasBeenInCreative": (9, 1),
    "pvp": (10, 1),
    "trustPlayers": (11, 1),
    "tnt": (12, 1),
    "fireSpreads": (13, 1),
    "hostCanFly": (14, 1),
    "hostCanChangeHunger": (15, 1),
    "hostCanBeInvisible": (16, 1),
    "bedrockFog": (17, 1),
    "disableSaving": (18, 1),
    "wasntSaveOwner": (19, 1),
    "worldSize": (20, 3),
    "mobGriefing": (23, 1),
    "keepInventory": (24, 1),
    "doMobSpawning": (25, 1),
    "doMobLoot": (26, 1),
    "doTileDrops": (27, 1),
    "naturalRegeneration": (28, 1),
    "doDaylightCycle": (29, 1),
}

@dataclass
class HostOptions:
    difficulty: Difficulty = Difficulty.normal
    friendsOfFriends: bool = False
    gamertags: bool = True # show player names above heads
    gameType: GameType = GameType.survival
    flatWorld: bool = False
    structures: bool = True
    bonusChest: bool = False
    hasBeenInCreative: bool = False
    pvp: bool = True
    trustPlayers: bool = True # players can build/mine without the host's permission
    tnt: bool = True
    fireSpreads: bool = True
    hostCanFly: bool = False
    hostCanChangeHunger: bool = False
    hostCanBeInvisible: bool = False
    bedrockFog: bool = False
    disableSaving: bool = False
    wasntSaveOwner: bool = False
    worldSize: WorldSize = WorldSize.classic
    mobGriefing: bool = True
    keepInventory: bool = False
    doMobSpawning: bool = True
    doMobLoot: bool = True
    doTileDrops: bool = True
    naturalRegeneration: bool = True
    doDaylightCycle: bool = True

    def toInt(self) -> int:
        value = 0
        for name, (shift, bits) in _LAYOUT.items():
            value |= (int(getattr(self, name)) & ((1 << bits) - 1)) << shift
        return value

    @classmethod
    def fromInt(cls, value:int) -> "HostOptions":
        options = cls()
        for field in fields(cls):
            shift, bits = _LAYOUT[field.name]
            raw = (value >> shift) & ((1 << bits) - 1)
            # Keep the field's type (enum or bool); an unknown enum value stays a plain int
            if field.type is bool:
                raw = bool(raw)
            elif raw in field.type._value2member_map_:
                raw = field.type(raw)
            setattr(options, field.name, raw)
        return options
