from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers  import FTPHandler
from pyftpdlib.servers import FTPServer
authorizer = DummyAuthorizer()

authorizer.add_user('haha', '12345',"/mnt/d/Code", perm='elradfmwMT')
handler = FTPHandler
handler.authorizer = authorizer

handler.passive_ports = range(21212, 65535)

server = FTPServer(('127.0.0.1', 21), handler)   
server.serve_forever()
