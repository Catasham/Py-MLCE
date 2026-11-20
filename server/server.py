import threading
import socket

from world.world import World
from server.serverProperties import ServerProperties
from net.tcpListener import TcpListener
from client.client import Client

# This file bridges connections to the world

#from net.Connection import Connection

class Server():
    def __init__(self, serverProperties:ServerProperties):
        self._serverProperties = serverProperties
        self._hostname = self._serverProperties.hostname
        self._port = int(self._serverProperties.port)
        self._world = World()

    def acceptClients(self):
        while self._running == True:
            connection, address = self._tcpListener.accept()
            print(f"Incoming connection: {address}")
            
            client = Client(connection, self._serverProperties)
            self._world.addClient(client)

    def run(self):
        print("Starting server")

        self._tcpListener = TcpListener(self._hostname, self._port)

        print(f"Binding to port {self._port}")
        self._tcpListener.bind()
        self._tcpListener.listen()

        self._running = True
        print("Server started")
        self.acceptClients()

    def updateProperty(self, key, newValue):
        self._serverProperties[key] = newValue