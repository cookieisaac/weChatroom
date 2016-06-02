from asyncore import dispatcher
import asyncore
import socket

class ChatServer(dispatcher):
    def handle_accept(self):
        conn, addr = self.accept()
        print ('Connection attempt from', addr[0])
    
PORT=5005
s = ChatServer()
s.create_socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', PORT))
s.listen(5)
asyncore.loop()