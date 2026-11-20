import threading
import socket

from client.client import Client

class World:
    def __init__(self):
        self._clients = []

    def connectClients(self):
        for client in self._clients:
            if client.connected == False:
                client.connect()

    def addClient(self, client:Client):
        self._clients.append(client)
        self.connectClients()