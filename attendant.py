class ParkingLot:
    def __init__(self, name, lat, lon, totalSpace, costHour):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.totalSpace = totalSpace
        self.availableSpace = totalSpace
        self.costHour = costHour

    def getSpace(self):
        return self.availableSpace

    def setBook(self):
        self.availableSpace -= 1


class signUp:
    def __init__(self, username, password):
        self.username = username
        self.password = password

#    def getDetails():
