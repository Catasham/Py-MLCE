import socket

class TcpListener():
    def __init__(self, hostname:str="0.0.0.0", port:int=25565, maxConnections:int=1):
        self._hostname = hostname
        self._port = port
        self._maxConnections = maxConnections

        # Create socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Prevent "Address already in use" errors on restart
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bind(self):
        self._socket.bind((self._hostname, self._port))

    def listen(self):
        self._socket.listen(self._maxConnections)

    def accept(self) -> tuple:
        client = self._socket.accept()
        return client