from _thread import start_new_thread
from pickle import dumps, loads
from socket import socket, AF_INET, SOCK_STREAM, gethostname, gethostbyname, error as socket_error

from game import Game, Player, Projectile


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
        except socket_error as err:
            print(err)
            return False

    def runServer(self):
        self.socket.listen(self.maxConnections)
        print("Server started, waiting for connections.")

        while True:
            connection, address = self.socket.accept()
            start_new_thread(self.threaded_client, (connection, address[0]))

        self.socket.close()

    def threaded_client(self, connection, address):
        username = connection.recv(128).decode("utf-8")
        print(f"{username} connected with adress: {address}")
        
        connection.send(dumps(self.game.joinPlayer(username)))
        self.playGame(connection)
        
        print(f"{username} disconnected with adress: {address}")
        self.game.killPlayer(username)
        connection.close()

    def playGame(self, connection):
        while True:
            try:
                if payload := loads(connection.recv(1024)):
                    self.processPayload(payload, connection)
                else:
                    break
            except Exception as err:
                print(err)
                break
            

    def processPayload(self, payload : Player or Projectile, connection):
        if isinstance(payload, Player):
            players, projectiles = self.game.updatePlayer(payload)
            connection.sendall(dumps((players, projectiles)))
        elif isinstance(payload, Projectile):
            self.game.updateProjectiles(payload)

if __name__ == '__main__':
    server = Server()
