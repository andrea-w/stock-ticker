from datetime import time

class GameRoom:
    def __init__(self, roomData):
        self.gameroomName = roomData.gameRoomName
        self.bondsPrice = 100
        self.grainPrice = 100
        self.industrialPrice = 100
        self.oilPrice = 100
        self.goldPrice = 100
        self.silverPrice = 100
        self.currentPlayers = []
        self.gameDuration = ''
        self.broker = roomData.playerIP
        self.startingCash = roomData.startingCash
        self.startingStocks = roomData.startingStockHoldings
        return
    
    def addPlayer(self,ip):
        self.currentPlayers.append(ip)
        return

    def getPlayers(self):
        return self.currentPlayers

    def setStartingCash(self, cash):
        self.startingCash = cash
        return

    def setStartingStocks(self, stocks):
        self.startingStocks = stocks
        return

    def setBondsPrice(self, price):
        self.bondsPrice = price
        return

    def setGrainPrice(self, price):
        self.grainPrice = price
        return

    def setIndustrialsPrice(self, price):
        self.industrialPrice = price
        return

    def setGoldPrice(self, price):
        self.goldPrice = price
        return

    def setSilverPrice(self, price):
        self.silverPrice = price
        return

    def setOilPrice(self, price):
        self.oilPrice = price
        return

    def getBrokerName(self):
        return self.broker

    def setGameRoomName(self, name):
        self.gameroomName = name
        return

    def getGameRoomName(self):
        return self.gameroomName

    def getBondsPrice(self):
        return self.bondsPrice

    def getGrainPrice(self):
        return self.grainPrice

    def getIndustrialsPrice(self):
        return self.industrialPrice

    def getGoldPrice(self):
        return self.goldPrice

    def getSilverPrice(self):
        return self.silverPrice

    def getOilPrice(self):
        return self.oilPrice

    def setGameDuration(self,duration):
        self.gameDuration = duration
        return

    def getGameDuration(self):
        return self.gameDuration

