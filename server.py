from _thread import start_new_thread
from pickle import dumps, loads
from socket import socket, AF_INET, SOCK_STREAM

from game import Game, Player, Projectile, GameEvent


class Server:
    def __init__(self):
        self.address = ("localhost", 5555)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.maxConnections = 5
        self.game = Game()
        
        start_new_thread(self.game.gameloop, ())

        if self.bindSocket():
            self.runServer()

    def bindSocket(self):
        try:
            self.socket.bind(self.address)
            return True
        except:
            return False

    def runServer(self):
        self.socket.listen(self.maxConnections)
        print("Server started, waiting for connections.")

        while True:
            connection, address = self.socket.accept()
            start_new_thread(self.threadedClient, (connection, address[0]))

        self.socket.close()

    def threadedClient(self, connection, address):
        username = loads(connection.recv(128))
        print(f"{username} connected with adress: {address}")
        
        connection.sendall(dumps(self.game.joinPlayer(username)))
        self.playGame(connection)
        
        print(f"{username} disconnected with adress: {address}")
        
        if username in self.game.players:
            self.game.killPlayer(username)
            del self.game.players[username], self.game.gameEvents[username]

    def playGame(self, connection):
        while True:
            try:
                if payload := loads(connection.recv(1024)):
                    if payload != "keep-alive":
                        self.processPayload(payload, connection)
                else:
                    break
            except:
                break
            
        connection.close()
            
    def processPayload(self, payload : Player or Projectile or GameEvent, connection):
        if isinstance(payload, Player):
            players, gameEvents = self.game.updatePlayer(payload)
            connection.sendall(dumps((players, gameEvents)))
        elif isinstance(payload, Projectile):
            self.game.updateProjectiles(payload)
        elif isinstance(payload, GameEvent) and payload.name == "player-respawn":
            connection.sendall(dumps(self.game.joinPlayer(payload.data)))

if __name__ == '__main__':
    server = Server()
