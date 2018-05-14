# Lobby.py
# The Lobby (only 1 exists) acts as server/controller for game

from flask import Flask, render_template, request, redirect, url_for
import socket
from GameRoom import GameRoom
from Player import Player

# pylint: disable=print-statement

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    #return "Ahoy there!"
    return render_template('home.html')

@app.route('/creategameroom', methods=['GET', 'POST'])
def createroom(data):
    if request.method == 'GET':
        return render_template('create-gameroom.html')
    elif request.method == 'POST':
        gameRoom = GameRoom(data)
        return redirect(url_for('play1'))

@app.route('/joingameroom')
def joinroom():
    return render_template('join-gameroom.html')

@app.route('/play/<string:gameRoomName>/')
def play1(gameRoomName):
      return render_template('play.html', gameRoomName=gameRoomName)

@app.route('/play/<string:gameRoomName>/', methods=['GET', 'POST'])
def play(gameRoomName):
    if request.method=='GET':
        return render_template('play.html', gameRoomName=gameRoomName)
    elif request.method=='POST':
        GameRoom.setGameRoomName = gameRoomName
        return redirect(url_for('play1', gameRoomName=gameRoomName))

if __name__ == '__main__':
    app.run(debug=True)

'''
Lobby controls the creation of gamerooms, creating new players 
(setting their names and connecting them to a particular gameroom)

Attributes:
    gameRoomNames
    currentPlayerIPs
    currentPlayerNames
    currentPlayers
    gameRooms
        for each gameRoom:
            - current prices of each stock
            - cash holdings of each player
            - stock holdings of each player
            - total wealth of each player
'''
class Lobby(object):
    def __init__(self):
        # return objects with no populated lists
        s = socket.socket()
        host = socket.gethostname()
        port = 9999
        address = (host, port)
        s.bind(address)
        s.listen(5)

        self.currentPlayerIPs = {}
        #self.currentPlayerNames = {}
        #self.currentPlayers = {}
        self.gameroomNames = []
        self.gameRooms = {}
        self.stocks = ['bonds', 'grain', 'industrial', 'oil', 'silver', 'gold']

        self.controlloop(s)
        return

    def getGameRoomNames(self):
        return self.gameroomNames

    '''
    Connects player with a specific gameroom
    '''
    def connectPlayer(self, gameroomName, playerIP):
        if gameroomName in self.gameroomNames:
            player = Player()
            self.gameRooms[gameroomName][playerIP] = player
            playerIP.sendall('Joined %s' % gameroomName)
        else:
            print("Could not connect. Room doesn't exist")
        return

    '''
    Creates new game room with given gameroomName
        - first checks that another gameroom with same name doesn't already exist
    Player who creates new room is assigned as broker
    '''
    def createGameRoom(self, gameroomName, playerIP):
        # check if room name is already taken
        if (gameroomName in self.gameroomNames):
            print("Cannot create. Room with that name already exists")
        else:
            newGameroom = GameRoom(playerIP, gameroomName)
            self.gameroomNames.append(gameroomName)
            self.gameRooms[gameroomName] = newGameroom
            self.gameRooms[gameroomName]['grain'] = 100
            self.gameRooms[gameroomName]['bonds'] = 100
            self.gameRooms[gameroomName]['industrial'] = 100
            self.gameRooms[gameroomName]['gold'] = 100
            self.gameRooms[gameroomName]['silver'] = 100
            self.gameRooms[gameroomName]['oil'] = 100
            self.gameRooms[gameroomName]['broker'] = playerIP
            playerIP.sendall('Confirm created room %s' % (gameroomName))
        return

    '''
    Returns the name associated with a given player's IP
    '''
    def getPlayerName(self, playerIP):
        return self.currentPlayerIPs[playerIP]

    '''
    Set a player's name to be assigned to their IP
    '''
    def setPlayerName(self, playerIP, playerName):
        self.currentPlayerIPs[playerIP] = playerName
        return

    '''
    This function receives a trade initiated by a player 
    '''
    def receiveTrade(self, gameroomName, playerIP, buy, stock, quantity):
        # buying
        if buy == 1:
            val = quantity * self.gameRooms[gameroomName][stock] / 100
            if self.gameRooms[gameroomName][playerIP]['cash'] < val:
                print "Error. Insufficient funds."
            else:
                self.gameRooms[gameroomName][playerIP]['cash'] -= val
                self.gameRooms[gameroomName][playerIP][stock] += quantity
                self.gameRooms[gameroomName][playerIP]['trade log'] += "bought %s %s at %s"  % (quantity, stock, self.gameRooms[gameroomName][stock])
                playerIP.sendall('Confirm purchase of %s shares of %s for %s' % (quantity, stock, val))
        # selling
        else:
            if self.gameRooms[gameroomName][playerIP][stock] < quantity:
                print "Error. Insufficient quantity to sell."
            else:
                val = quantity * self.gameRooms[gameroomName][stock] / 100
                self.gameRooms[gameroomName][playerIP]['cash'] += val
                self.gameRooms[gameroomName][playerIP][stock] -= quantity
                self.gameRooms[gameroomName][playerIP]['trade log'] += "sold %s %s at %s" % (quantity, stock, self.gameRooms[gameroomName][stock])
                playerIP.sendall('Confirm sale of %s shares of %s for %s' % (quantity, stock, val))
        return
    
    '''
    Send dividends payment to each player
    '''
    def payDividends(self, gameroomName, price, stock):
        if self.gameRooms[gameroomName][stock] < 100:
            print 'Stock price too low to pay dividend'
            return
        for player in self.gameRooms[gameroomName]['players']:
            payment = self.gameRooms[gameroomName][player][stock] * price / 100
            self.gameRooms[gameroomName][player]['cash'] += payment
            self.gameRooms[gameroomName][player]['total worth'] += payment
            player.sendall('div,%s,%s,%s,%s' % (payment, self.gameRooms[gameroomName][player][stock], stock, price))
        return

    '''
    Receive updated stock price from broker
    '''
    def receiveUpdatedStockPrice(self, gameroomName, stock, price):
        if (stock in self.stocks):
            if (0 < price & price < 200):

                self.gameRooms[gameroomName][stock] = price

                for player in self.gameRooms[gameroomName]['players']:
                    value = self.gameRooms[gameroomName][player][stock] * price / 100
                    self.gameRooms[gameroomName][player]['total worth'] = self.calculateTotalWorth(player, gameroomName)            
        
                clients = self.gameRooms[gameroomName]['players']
                for i in clients:
                    i.sendall('price,%s,%s,worth,%s' % (stock, price, self.gameRooms[gameroomName][i]['total worth']))
            elif price==200:
                self.gameRooms[gameroomName][stock] = 100

                for player in self.gameRooms[gameroomName]['players']:
                    self.gameRooms[gameroomName][player][stock] *= 2
                    value = self.gameRooms[gameroomName][player][stock] * price / 100
                    self.gameRooms[gameroomName][player]['total worth'] = self.calculateTotalWorth(player, gameroomName)            
        
                clients = self.gameRooms[gameroomName]['players']
                for i in clients:
                    i.sendall('price,%s,%s,worth,%s' % (stock, price, self.gameRooms[gameroomName][i]['total worth']))
            elif price==0:
                self.gameRooms[gameroomName][stock] = 100

                for player in self.gameRooms[gameroomName]['players']:
                    self.gameRooms[gameroomName][player][stock] = 0
                    value = self.gameRooms[gameroomName][player][stock] * price / 100
                    self.gameRooms[gameroomName][player]['total worth'] = self.calculateTotalWorth(player, gameroomName)            
        
                clients = self.gameRooms[gameroomName]['players']
                for i in clients:
                    i.sendall('price,%s,%s,worth,%s' % (stock, price, self.gameRooms[gameroomName][i]['total worth']))
        else: print 'Could not parse stock name %s' % (stock)
        return

    '''
    Calculate total worth of player
    '''
    def calculateTotalWorth(self, playerIP, gameRoomName):
        val = 0
        for stock in self.stocks:
            val += self.gameRooms[gameRoomName][playerIP][stock] * self.gameRooms[gameRoomName][stock] / 100
        return val

    '''
    Having received message from player/broker, this
    method can be called to parse the message, then calls
    appropriate method above

    T = make player's trade
    U = update stock price
    P = pay dividends
    S = set up game room
    '''
    def parsePlayerMessage(self, message):
        if message.startsWith("T"):
            a,b,c,d,e,f = message.split(",")
            gameroomName = b
            playerIP = c
            buy = d
            stock = e
            quantity = f
            self.receiveTrade(gameroomName, playerIP, buy, stock, quantity)

        elif message.startsWith("U"):
            a,b,c,d = message.split(",")
            gameroomName = b
            stock = c
            price = d
            
            self.gameRooms[gameroomName][stock] = price

        elif message.startsWith("P"):
            a,b,c,d = message.split(",")
            gameroomName = b
            stock = c
            price = d

            self.payDividends(gameroomName, price, stock)

        elif message.startsWith("S"):
            a,b,c,d,e = message.split(",")
            gameroomName = b
            duration = c
            startingCash = d
            startingHoldings = e

            self.gameRooms[gameroomName]['duration'] = duration
            for player in self.gameRooms[gameroomName]['players']:
                self.gameRooms[gameroomName][player]['cash'] = startingCash
                self.gameRooms[gameroomName][player]['grain'] = startingHoldings
                self.gameRooms[gameroomName][player]['industrial'] = startingHoldings
                self.gameRooms[gameroomName][player]['bonds'] = startingHoldings
                self.gameRooms[gameroomName][player]['oil'] = startingHoldings
                self.gameRooms[gameroomName][player]['gold'] = startingHoldings
                self.gameRooms[gameroomName][player]['silver'] = startingHoldings


        else: print "Error - cannot parse message: %s" % message
        return

    def setBondsPrice(self,price, gameroomName):
        self.gameRooms[gameroomName]['bonds'] = price
        return

    def setGrainPrice(self,price, gameroomName):
        self.gameRooms[gameroomName]['grain'] = price
        return

    def setIndustrialsPrice(self,price, gameroomName):
        self.gameRooms[gameroomName]['industrial'] = price
        return

    def setGoldPrice(self,price, gameroomName):
        self.gameRooms[gameroomName]['gold'] = price
        return

    def setSilverPrice(self,price, gameroomName):
        self.gameRooms[gameroomName]['silver'] = price
        return

    def setOilPrice(self,price, gameroomName):
        self.gameRooms[gameroomName]['oil'] = price
        return
    
    def getBondsPrice(self,gameroomName):
        return self.gameRooms[gameroomName]['bonds']

    def getGrainPrice(self,gameroomName):
        return self.gameRooms[gameroomName]['grain']

    def getIndustrialsPrice(self,gameroomName):
        return self.gameRooms[gameroomName]['industrial']

    def getGoldPrice(self,gameroomName):
        return self.gameRooms[gameroomName]['gold']

    def getSilverPrice(self,gameroomName):
        return self.gameRooms[gameroomName]['silver']

    def getOilPrice(self,gameroomName):
        return self.gameRooms[gameroomName]['oil']  

    def controlloop(self, s):
        while True:
            client, address = s.accept()
            message = client.recv(1024)
            print("Received message "+message)

            if message is not None:
                self.parsePlayerMessage(message)
            
            message = None
            address = None
