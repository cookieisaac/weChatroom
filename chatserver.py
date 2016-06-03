from asyncore import dispatcher
import asyncore
import socket
from chatsession import ChatSession
from chatroom import ChatRoom

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
        
        self.users = {}
        self.name  = name
        self.main_room = ChatRoom(self)

    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self, conn)
        
    
if __name__ == "__main__":
    s = ChatServer(PORT, NAME)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass
        