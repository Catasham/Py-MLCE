from core.binaryReader import BinaryReader
from core.binaryWriter import BinaryWriter

from protocol.packet import Packet, PacketId, MAGIC
from protocol.packetHandler import PacketHandler
from protocol.framePacket import FramePacket

# For encoding/decoding frame packets
class FramePacketHandler(PacketHandler):

    # Yields packets from frame
    def readPacketsFromFrame(self):

        # number of bytes in frame
        length = self._reader.readU32()

        readFrame = True
        while readFrame:
            
            """        # Length 0 means the stream is unframed, so it should be processed differently
                    # There is only one packet in an unframed stream
                        if length == 0: 
                            # Only parse if unframed stream has arrived
                            if self._reader.bufferSize > 0:
                                packet = self._parsePacket()
                                yield packet
                                # Exit loop after parsing one packet
                                readFrame = False
                            else:
                                # Yield none if there is no data to parse
                                yield None
                        else:"""

            # Extract all packets from frame once the frame is complete
            if length <= self._reader.bufferSize:
                while self._reader.bufferSize > 0:
                    packet = self._parsePacket()
                    yield packet

                    while self._reader.bufferSize == 0: yield None
                    # reset length after new data arrives
                    length = self._reader.readU32()

            else:
                # Return nothing if there is no complete data to read
                # Will be called again when there is more data in the buffer
                yield None

        return None

    """    # Yields fully completed packets after they arrive
        def readPacket(self):

            packet:Packet
        
            # Reads data until there is no more
            frameReader = self._readFrame()
            for packetData in frameReader:

                # Do not parse packet if there is no data
                if packetData == None:
                    yield None
                else:
                    # Parse packet
                    packet = self._handlePacket()
                    yield packet

            raise StopIteration"""