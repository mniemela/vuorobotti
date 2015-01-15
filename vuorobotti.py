# -*- coding: iso-8859-1 -*-

import socket
import botcommands
import threading
from threading import Timer
import sys
import sched, time
import settings

#onkelmia: ctrl-c ei lopeta threadeja, eik� tajua reconnectata jos yhteys
#katkeaa. lis�ksi ei tajua vaihtaa nikki� jos nikki rekister�ity


class Ircbot:

    def __init__( self):


        # v�ltt�m�tt�mi� tietoja

        self.server   = settings.server
        self.port     = settings.port
        self.username = settings.name
        self.realname = settings.name
        self.nick     = settings.nick
        self.msgcount = 0

        # luodaan socketit

        self.socket   = socket.socket()
        self.listensocket = socket.socket()
        
        # haetaan botille komennot

        self.commands = botcommands.command_dict

        # p��looppia toistettan kunnes done = 1

        self.done     = 0

        # kanava jolle botti halutaan

        self.channel  = settings.channel

        self.tmr = Timer(60, self.clearCounter, ())
        self.tmr.start()

    #nollataan sp�mminestolaskuri
    def clearCounter(self):
        self.msgcount = 0
        self.tmr = Timer(60, self.clearCounter, ())
        self.tmr.start()

    def send( self, string ):

        self.socket.send( (string + '\r\n'))

    #l�hett�� viestin, jos l�hetetty 6 viesti� minuutissa, ei tee mit��n
    def sendmsg( self, string):

        if self.msgcount < 10:
            self.msgcount += 1
            self.send(('PRIVMSG %s :' % self.channel) + string)

    def sendnotice( self, string):

        if self.msgcount < 6:
            self.msgcount += 1
            self.send(('NOTICE %s :' % self.channel) + string)

    def connect( self ):
        self.listensocket.bind(('localhost', 666))
        self.listensocket.listen(5)
        self.socket.connect( ( self.server, self.port ) )
        self.send( 'NICK %s' % self.nick )
        self.send( 'USER %s a a :%s' % ( self.username, self.realname ) )

        self.send( 'JOIN %s' % self.channel )
    
    def sendTurnChangeMsg(self, conn):
        print "yhteys"
        while True:
            data = conn.recv(2048)
            print data
            if not data:
                break
            else:
                self.sendmsg(data)
        conn.close()
    
    def listenTurnChange(self):
        while not self.done:
            conn, addr = self.listensocket.accept()
            print "avataan yhteys"
            t = threading.Thread(target=self.sendTurnChangeMsg, args=(conn,))
            t.start()

    def check( self, line ):

        print line
        line = line.split(' ')

        # vastataan pingiin muuten serveri katkaisee yhteyden

        if line[0] == 'PING':

             self.send( 'PONG :abc' )

        elif len(line) > 1 and (line[1] == '437' or line[1] == '433'):
        
            if self.nick == settings.nick2:
                self.send( 'QUIT')
                self.socket.close()
                self.done = 1
            else:
                self.nick = settings.nick2
                self.send( 'NICK %s' % self.nick )
                self.send( 'JOIN %s' % self.channel )
        try:

            if line[2][0] != '#':

                return


            # suoritetaan komennot jos niit� on tullut

            self.commands[ line[3] ].main( self , line )

        except:

            pass


    def mainloop( self ):

        buffer = ''

        while not self.done:

            # vastaanotetaan dataa
            
            buffer += self.socket.recv( 4096 )
            buffer = buffer.split( '\r\n' )

            
            for line in buffer[0:-1]:

                self.check( line )

            buffer = buffer[-1]
            

        print "Suljetaan botti..."
        self.tmr.cancel()

class Input():

    def __init__(self):
        self.irc = None

    def setBot(self, irc):
        self.irc = irc
    
    def read_keyboard(self):
        
        command = ""
        if self.irc is not None:
            while True:
                command = sys.stdin.readline().lower().rstrip()
                print command
                if command == 'quit':
                    self.irc.send( 'QUIT' )
                    self.irc.socket.close()
                    self.irc.done = 1
                    break;

def main():

    input = Input()
    thread_input = threading.Thread(target=input.read_keyboard)
    
    irc = Ircbot()
    input.setBot(irc)

    irc.connect()
    
    thread = threading.Thread(target=irc.listenTurnChange)
    thread_input.start()
    thread.start()
    irc.mainloop()
    try:
        thread_input._Thread__stop()
    except:
        print(str(thread_input.getName()) + ' could not be terminated')
    try:
        thread._Thread__stop()
    except:
        print(str(thread.getName()) + ' could not be terminated')
    sys.exit()

if __name__ == '__main__': main()
