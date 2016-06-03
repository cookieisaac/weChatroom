class CommandHandler:
    def unknown(self, session, cmd, params):
        session.push('Unknown command: %s with parameter %s\r\n'%(cmd, params))
    
    def handle(self, session, line):
        if not line.strip(): 
            return
        
        args = line.split(' ', 1)
        cmd = args[0]
        try: 
            params = args[1].strip()
        except IndexError:
            params = ''
        
        method_name = 'do_' + cmd
        method = getattr(self, method_name, None)
        
        print(method)
        print("method_name: "+method_name)
        try:
            method(session, params)
        except TypeError:
            print("TypeError caught")
            self.unknown(session, cmd, params)   
 
 
class EndSession(Exception):
    pass
    
class Room(CommandHandler):
    def __init__(self, server):
        self.server = server
        self.sessions = []
        
    def add(self, session):
        self.sessions.append(session)
        
    def remove(self, session):
        self.sessions.remove(session)
        
    def broadcast(self, line):
        for session in self.sessions:
            session.push(line)
            
    def do_logout(self, session, line):
        raise EndSession()
        
class LoginRoom(Room):
    def add(self, session):
        Room.add(self, session)
        self.broadcast('Welcome to %s\r\n' % self.server.name)
        
    def unknown(self, session, cmd, params):
        Room.unknown(self, session, cmd, params)
        session.push('Please log in with format "login ike"\r\n')
        
    def do_login(self, session, params):
        name = params.strip()
        if not name:
            session.push('Please enter a name\r\n')
        elif name in self.server.users:
            session.push('The name %s is taken.\nPlease use another name.\r\n' % name)
        else:
            session.name = name
            session.enter(self.server.main_room)
            
class ChatRoom(Room):
    def add(self, session):
        self.broadcast(session.name + ' has entered the room.\r\n')
        self.server.users[session.name] = session
        Room.add(self, session)
        
    def remove(self, session):
        Room.remove(self, session)
        self.broadcast(session.name + ' has left the room.\r\n')
        
    def do_say(self, session, line):
        self.broadcast(session.name+': ' + line+'\r\n')
        
    def do_look(self, session, params):
        session.push('The following are in this room:\r\n')
        for other in self.sessions:
            session.push(other.name+'\r\n')
            
    def do_who(self, session, params):
        session.push('The follwing are logged in:\r\n')
        for name in self.server.users:
            session.push(name + '\r\n')
            
class LogoutRoom(Room):
    def add(self, session):
        try:
            del self.server.users[session.name]
        except KeyError:
            pass
            
            
            