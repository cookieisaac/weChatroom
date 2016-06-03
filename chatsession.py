from asynchat import async_chat
import asynchat
from chatroom import LoginRoom, LogoutRoom, EndSession

class ChatSession(async_chat):
    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        self.set_terminator('\r\n')
        self.data = []
        self.server = server
        self.name = None
        self.enter(LoginRoom(server))
        
    def enter(self, room):
        try: 
            current_room = self.room
        except AttributeError:
            pass
        else:
            current_room.remove(self)
            
        self.room = room
        room.add(self)       
        
    def collect_incoming_data(self, data):
        self.data.append(data)
        
    def found_terminator(self):
        line = "".join(self.data)
        self.data = []
        try: 
            self.room.handle(self, line)
        except EndSession:
            self.handle_close()
            
    def handle_close(self):
        async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))