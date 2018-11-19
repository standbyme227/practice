import socketserver
import threading

HOST = ''
PORT = 9009
lock = threading.Lock()


class UserManager:
    def __init__(self):
        self.users = {}

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())

    def addUser(self, username, conn, addr):
        if username in self.users:
            conn.send('이미 등록된 사용자 입니다.\n'.encode())
            return None

        lock.acquire()
        self.users[username] = (conn, addr)
        lock.release()

        self.sendMessageToAll('{}님이 입장했습니다.'.format(username))
        print('+++ 대화 참여자 수 {}'.format(len(self.users)))
        return username

    def removeUser(self, username):
        if username not in self.users:
            return
        lock.acquire()
        del self.users[username]
        lock.release()

        self.sendMessageToAll('{}님이 퇴장했습니다.'.format(username))
        print('+++ 대화 참여자 수 {}'.format(len(self.users)))

    def messageHandler(self, username, msg):
        if msg[0] != '/':
            self.sendMessageToAll('[{}] {}'.format(username, msg))
        if msg.strip() == '/quit':
            self.removeUser(username)
            return -1


class MyTcpHandler(socketserver.BaseRequestHandler):
    usermanager = UserManager()

    def registerUsername(self):
        while True:
            self.request.send('로그인ID'.encode())
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.usermanager.addUser(username, self.request, self.client_address):
                return username

    def handle(self):
        print('{} 연결됨'.format(self.client_address[0]))

        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
                print(msg.decode())
                if self.usermanager.messageHandler(username, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)

        except Exception as e:
            print(e)
        print("[{}] 접속종료".format(self.client_address[0]))
        self.usermanager.removeUser(username)


class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def runServer():
    print('+++ 채팅 서버를 시작합니다.')
    print('+++ 채팅 서버를 끝내려면 Ctrl-C를 누르세요')

    try:
        server = ChatingServer((HOST, PORT), MyTcpHandler)
    except KeyboardInterrupt:
        print("--- 채팅서버를 종료합니다.")
        server.shutdown()
        server.server_close()


runServer()
