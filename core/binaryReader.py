import struct
from core.structData import DataTypeSizes, DataTypeStructId

class BinaryReader():
    def __init__(self, buffer:bytearray):
        self._buffer = buffer

    def addToBuffer(self, b:bytearray):
        self._buffer.extend(b)

    def _read(self, valueType, be=True, valueSize=None, valueIdentifier=None):
        # Get size and struct (module) identifier for the value
        if not valueSize: valueSize = DataTypeSizes[valueType].value
        if not valueIdentifier: valueIdentifier = DataTypeStructId[valueType].value

        # Read data
        # Add string length before identifier if it exists
        value = struct.unpack(f"{">" if be else "<"}{valueSize if valueIdentifier==DataTypeStructId["string_t"].value else ""}{valueIdentifier}", self._buffer[:valueSize])[0]

        # Remove value from data
        del self._buffer[:valueSize]

        return value
        
    # Read methods
    def readBytes(self, length) -> bytearray:
        value = self._buffer[:length]
        del self._buffer[:length]
        return value
    def readBool(self) -> bool: return self._read("bool_t")
    def readI8(self) -> int: return self._read("i8_t")
    def readU8(self) -> int: return self._read("u8_t")
    def readI16(self, be=True) -> int: return self._read("i16_t", be=be)
    def readU16(self, be=True) -> int: return self._read("u16_t", be=be)
    def readI32(self, be=True) -> int: return self._read("i32_t", be=be)
    def readU32(self, be=True) -> int: return self._read("u32_t", be=be)
    def readI64(self, be=True) -> int: return self._read("i64_t", be=be)
    def readU64(self, be=True) -> int: return self._read("u64_t", be=be)
    def readFloat(self, be=True) -> float: return self._read("float_t", be=be)
    def readDouble(self, be=True) -> float: return self._read("double_t", be=be)
    def readChar(self) -> str: return self._read("char_t")
    def readAsciiFixed(self, stringSize, be=True) -> str: return self._read("string_t", be=be, valueSize=stringSize)

    def readUtf16(self, be=True) -> None:
        readLength = self.readU16(be=be)
        encodedString = self.readBytes(readLength * 2) # Multiplied by two because each character is two bytes
        decodedString = encodedString.decode("utf-16-be")

        return decodedString

    def release(self):
        self._buffer = bytearray()

    @property
    def bufferSize(self) -> int:
        return len(self._buffer)

    @property
    def buffer(self) -> bytearray:
        return self._buffer