import sys, socket, random, os, select

# pylint: disable=print-statement

class Player():
    def __init__(self):
        ##
        ## instance of Client stores info:
        ##		ip - user's IP address
        ##		alias - user's current alias
        ## when new Client first created, by default they are assigned an alias of a random alphanumeric string
        ##
        self.ip = socket.gethostbyname(socket.gethostname())
        self.alias = os.urandom(16)
        self.port = random.randint(5000, 90000)
        self.host = socket.gethostname()
        self.gameroomName = None

        self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_conn.connect(self.host, self.port)

        self.list_sockets = [sys.stdin, self.server_conn]


        ## listen to receive messages from Lobby server
        while True:
            self.read_sockets, self.write_sockets, self.error_sockets = select.select(self.list_sockets, [], [])
            for sock in self.read_sockets:
                if sock is self.server_conn:
                   msg = sock.recv()
                   print msg
                   self.parseFromServer(msg)
            for wr in self.write_sockets:
                self.server_conn.sendall(sys.stdin.readline())

    '''
    Create tuple for trade where index:
    buy = 1, sell = 0
    stock is name of stock
    quantity is quantity of stock to buy/sell

    Players & broker have permission to call this
    '''
    def makeTrade(self, buy, stock, quantity):
        for wr in self.write_sockets:
            self.server_conn.sendall("T,"+self.gameroomName +self.ip+"Buy"+buy+"Stock"+stock+"Quantity"+quantity)
        return


    '''
    Only broker has permission to call this
    '''
    def updateStockPrice(self, stock, price):
        for wr in self.write_sockets:
            self.server_conn.sendall("U,"+self.gameroomName +stock+"Price"+price)
        return


    '''
    Only broker has permission to call this
    '''
    def sendDividendsInfo(self, stock, price):
        for wr in self.write_sockets:
            self.server_conn.sendall("P,"+self.gameroomName +stock+"Price"+price)
        return

    '''
    Only broker has permission to call this
    '''
    def setUpGameRoom(self, duration, startingCash, startingHoldings):
        for wr in self.write_sockets:
            self.server_conn.sendall("S,"+self.gameroomName +duration+"StartingCash"+startingCash+"StartingHoldings"+startingHoldings)
        return

    def setName(self, playerName):
        self.alias = playerName
        return

    def getName(self):
        return self.alias

    def parseFromServer(self, msg):
        if msg.startswith('div'):
            self.receiveDividend(msg)
        elif msg.startswith('Confirm'):
            print msg
        elif msg.startswith('Join'):
            print msg
            a, b = msg.split(" ")
            self.gameroomName = b
        return

    def receiveDividend(self, msg):
        a, b, c, d, e = msg.split(',')
        print 'Received payment of %s for %s shares of %s at %s each' % (b, c, d, e)
        return

def main():

    player = Player()

if __name__ == "__main__":
    main()
