# -*- coding: iso-8859-1 -*-

import random
import dom4status
import settings

# tähän sanastoon lisätään komennot ja niitä vastaavat oliot

command_dict = {}



class Vuoro:

    def askturn(self, i, irc):
        try:
            data = dom4status.query(settings.domserver, settings.ports[i])
            irc.sendmsg(settings.games[i] + 'n vuoro ' + str(data.turn) + ' menossa, ' + str(data.timer / 3600000) + 'h aikaa tehdä vuoro.')
        except:
            pass

    def main(self, irc, line):
        if len(line) < 5:
            for i in range(len(settings.games)):
                self.askturn(i, irc)
        else:
            for i in range(len(settings.games)):
                if line[4] == settings.games[i]:
                    self.askturn(i, irc)
        
command_dict[ ':!vuoro' ] = Vuoro()

class Kukalagaa:

    def asklaggers(self, i, irc): 
        try:
            data = dom4status.query(settings.domserver, settings.ports[i])
            laggers = []
            msg = ""
            for n in data.nations:
                if n.submitted != 2 and n.statusnum == 1:
                    print n.name
                    laggers.append(settings.players[i][n.name])
            if len(laggers) > 1:
                for j in range(len(laggers)):
                    if len(laggers) - j > 1:
                        msg += (laggers[j] + ', ')
                        print msg
                    else:
                        msg += laggers[j]
                        print msg
                msg += (' lagaavat ' + settings.games[i] + 'ssä!')
            else:
                msg += (laggers[0] + ' lagaa ' + settings.games[i] + 'ssä!')
            irc.sendmsg(msg)            
        except:
            pass
            
    def main(self, irc, line):
        if len(line) < 5:
            for i in range(len(settings.games)):
                self.asklaggers(i, irc)
        else:
            for i in range(len(settings.games)):
                if line[4] == settings.games[i]:
                    self.asklaggers(i, irc)
                        

command_dict[ ':!kukalagaa' ] = Kukalagaa()