commands = {
    "/say CONTENT": "say something",
    "/login NAME": "login to server",
    "/logout": "logout of server",
    "/look": "look who is in current room",
    "/who": "who has login to the server",
    "/where": "which room I am in right now",
    "/list": "list all currently supported commands",
    "/rooms": "list all rooms available in the server",
    "/new ROOM": "create a new room",
    "/enter ROOM": "enter a room",
    "/exit": "exit current room and go back to Main Lobby",
    "/delete ROOM": "delete a room",
}

class CommandHandler:
    def unknown(self, session, cmd, params):
        session.push('Unknown command: %s with parameter %s\r\n'%(cmd, params))
    
    def handle(self, session, line):
        if not line.strip(): 
            return
        
        if line.strip().startswith('/'):
            args = line.split(' ', 1)
            cmd = args[0][1:]
            try: 
                params = args[1].strip()
            except IndexError:
                params = ''
        else:
            cmd = 'say'
            params = line.strip()
        
        method_name = 'do_' + cmd
        method = getattr(self, method_name, None)
        
        print(method)
        print("method_name: "+method_name)

        try:
            method(session, params)
        except TypeError as e:
            print("TypeError caught" + str(e))
            self.unknown(session, cmd, params)   
    
 
class EndSession(Exception):
    pass
    
class Room(CommandHandler):
    def __init__(self, server, name):
        self.server = server
        self.name = name
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
        self.broadcast('Welcome to %s Service\r\n' % self.server.server_name)
        self.broadcast('Please login first with command "/login myname"\r\n')
        
    def unknown(self, session, cmd, params):
        Room.unknown(self, session, cmd, params)
        session.push('Please log in with format "/login ike"\r\n')
        
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
        session.push('***Welcome to room %s. Start chatting right away, or use "/list" to see all avalable commands.***\r\n' % self.name)
        self.broadcast(session.name + ' has entered the room %s.\r\n' % self.name)
        self.server.users[session.name] = session
        Room.add(self, session)
        
    def remove(self, session):
        Room.remove(self, session)
        self.broadcast(session.name + ' has left the room %s.\r\n' % self.name)
        
    def do_say(self, session, line):
        self.broadcast('%s@%s: %s\r\n'% (session.name, self.name, line))
        
    def do_look(self, session, params):
        session.push('The following are in this room %s:\r\n' % self.name)
        for other in self.sessions:
            session.push(other.name+'\r\n')
            
    def do_who(self, session, params):
        session.push('The follwing are logged in:\r\n')
        for name in self.server.users:
            session.push(name + '\r\n')
            
    def do_list(self, session, params):
        session.push('The following command are supported:\r\n')
        for cmd, description in commands.items():
            session.push('{0:20} {1}\r\n'.format(cmd, description))

    def do_where(self, session, params):
        session.push('You are currently in room "%s".\r\n' % self.name)
        
    def do_enter(self, session, params):
        try:
            room = self.server.rooms[params]
        except KeyError:
            session.push("Room %s has not been created yet.\r\n" % params)
        else:    
            session.enter(room)
        
    def do_rooms(self, session, params):
        session.push('The following rooms are available:\r\n')
        for roomname in self.server.rooms:
            session.push(roomname+'\r\n')
            
    def do_new(self, session, params):
        if params in self.server.rooms:
            session.push("Room %s has already been created.\r\n" % params)
        else:
            try:
                session.server.rooms[params] = ChatRoom(session.server, params)
            except Exception as e:
                session.push("Fail to create room %s\r\n" % params)
            else:
                session.push('New chat room "%s" created\r\n' % params)
    
    def do_exit(self, session, params):
        self.do_enter(session, "Main Lobby")
        
    def do_delete(self, session, params):
        if params not in self.server.rooms:
            session.push("Room %s does not exist.\r\n" % params)
        else:
            room = self.server.rooms[params]
            if room.sessions != []:
                session.push("Cannot delete due to member(s) %s still being active in this room.\r\n" % str([user.name for user in room.sessions]))
            else:
                del self.server.rooms[params]
                session.push("Room %s has been deleted.\r\n" % params)
            
class LogoutRoom(Room):
    def add(self, session):
        try:
            del self.server.users[session.name]
        except KeyError:
            pass
            
            
            