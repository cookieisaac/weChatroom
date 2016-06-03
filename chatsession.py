from asynchat import async_chat

class ChatSession(async_chat):
    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        self.set_terminator('\r\n')
        self.data = []
        self.server = server
        
        self.push('Welcome to %s\r\n' % self.server.name)
        
    def collect_incoming_data(self, data):
        self.data.append(data)
        
    def found_terminator(self):
        line = "".join(self.data)
        self.data = []
        print line