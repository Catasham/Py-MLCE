class ServerProperties():
    def __init__(self, filePath):
        self._filePath = filePath

        self._properties = {
            "port": 25565,
            "hostname": "0.0.0.0",
            "maxPlayers": 10,
            "netcodeVersion": 560
        }

    def _setProperty(self, name, value):
        self._properties[name] = value

    def _getProperty(self, propertyName):
        if propertyName in self._properties:
            return self._properties[propertyName]
        else:
            raise AttributeError("")

    def read(self):
        with open(self._filePath, "r") as file:
            fileData = file.read()
            fileLines = fileData.split("\n")

            properties = {}

            # Read each line and assign property
            for line in fileLines:
                propertyName, propertyValue = line.split("=")
                self._setProperty(propertyName, propertyValue)

    @property
    def port(self):
        return self._getProperty("port")

    @property
    def hostname(self):
        return self._getProperty("hostname")

    @property
    def maxPlayers(self):
        return self._getProperty("maxPlayers")