from asyncore import dispatcher
import asyncore
import socket
from chatsession import ChatSession

NAME='WeChatroom'
PORT=5005

class ChatServer(dispatcher):
    def __init__(self, port, name):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        #With this call, the port is available immediately to other processes (new server) after current server crash
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        
        self.sessions = []
        self.name  = name

    def handle_accept(self):
        conn, addr = self.accept()
        self.sessions.append(ChatSession(self, conn))
        print ('Connection attempt from', addr[0])
        
    def disconnect(self, session):
        self.sessions.remove(session)
        
    def broadcast(self, line):
        for session in sessions:
            self.push(line + '\r\n')
    
    
if __name__ == "__main__":
    s = ChatServer(PORT, NAME)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass
        