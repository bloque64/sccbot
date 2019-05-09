
import discord
from discord.ext import commands
import sys
import unittest
sys.path.append("../sccbot")
import data as data
from data import User
from settings import Settings
from register import UserRegisterer
from xmlrpc.server  import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading

TEST_VERIFICATION_TOKEN = "74875725480c3eb46912c1bbbfbcc9d6"

settings_path = "../config/"
sa_session = data.return_session()
settings = Settings(sa_session, settings_path)


settings_path = "../config/"
sa_session = data.return_session()
settings = Settings(sa_session, settings_path)

# https://github.com/jagrosh/MusicBot/wiki/Adding-Your-Bot-To-Your-Server

def exit_gracefully():

    print("Quiting sccbot...")

class StoppableThreadingXMLRPCServer(
    ThreadingTCPServer, SimpleXMLRPCDispatcher, threading.Thread
):
    
    def __init__(
        self, addr, requestHandler = SimpleXMLRPCRequestHandler, logRequests = True
    ):
        self.logRequests = logRequests
        if sys.version_info[:2] < (2, 5):
            SimpleXMLRPCDispatcher.__init__(self)
        else:
            SimpleXMLRPCDispatcher.__init__(self, allow_none = False, encoding = None)
        ThreadingTCPServer.__init__(self, addr, requestHandler)
        threading.Thread.__init__(self)
    
    
    def run(self):
        # *serve_forever* muss in einem eigenen Thread laufen, damit man es
        # unterbrechen kann!
        self.serve_forever()
        print "Thread beendet"
    
    
    def stop(self):
        self.shutdown()


class XmlrpcHandler:
    
    def __init__(self, server):
        self._server = server
    
    
    def get_time(self):
        time.sleep(0.2) # nur zum Testen der Threads!
        return time.asctime()
    
    
    def close(self, password):
        if password == "12345":
            self._stoptimer = threading.Timer(1, self._server.stop)
            self._stoptimer.start()
            return "Befehl zum Stoppen erteilt"
        return "falsches Passwort - Server wird nicht gestoppt"


def main():
    
    server = StoppableThreadingXMLRPCServer(("localhost", 50505), logRequests = True)
    handler = XmlrpcHandler(server)
    server.register_instance(handler)
    
    print "Der XMLRPC-Server horcht auf http://localhost:50505."
    print "Er kann mit STRG+C oder STRG+PAUSE beendet werden."
    print
    
    server.start()
    try:
        while server.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        server.stop()


""" if __name__ == "__main__":
    main()

bot1 = bot = commands.Bot(command_prefix="!")
try:
    server = ServerThread()
    server.start() # The xml rpc server is now running
    print("XML RPC server started in its own thread")
    bot1.run("")
    print("Discord bot started")
except KeyboardInterrupt:
    pass
finally:
    exit_gracefully() """


