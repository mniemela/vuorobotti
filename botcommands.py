﻿# -*- coding: utf-8 -*-

import random
import dom4status
import settings
import filereader

# tähän sanastoon lisätään komennot ja niitä vastaavat oliot

command_dict = {}



class Vuoro:

    def askturn(self, name, port, irc):
        try:
            data = dom4status.query(settings.domserver, port)
            irc.sendmsg(name + 'n vuoro ' + str(data.turn) + ' menossa, ' + str(data.timer / 3600000) + 'h aikaa tehda vuoro.')
        except:
            irc.sendmsg("Virhe! " + name + "n servuun ei saa yhteyttä!")

    def main(self, irc, line):
        f = filereader.read(settings.teamfile)
        if len(line) < 5:
            for i in range(len(f)):
                self.askturn(f[i].name, f[i].port, irc)
        else:
            for i in range(len(f)):
                if line[4] == f[i].name:
                    self.askturn(f[i].name, f[i].port, irc)
        
command_dict[ ':!vuoro' ] = Vuoro()

class Kukalagaa:

    def asklaggers(self, name, port, players, irc): 
        try:
            data = dom4status.query(settings.domserver, port)
            laggers = []
            desuralaggers = 0
            msg = ""
            for n in data.nations:
                if n.submitted != 2 and (n.statusnum == 1 or n.statusnum == 254) and n.name in players:
                    print players[n.name]
                    laggers.append(players[n.name])
                elif n.submitted != 2 and (n.statusnum == 1 or n.statusnum == 254):
                    desuralaggers += 1
            if (len(players) < len(data.nations) and desuralaggers > 0):
                laggers.insert(0, "Desura")
            if len(laggers) > 1:
                for j in range(len(laggers)):
                    if len(laggers) - j > 1:
                        msg += (laggers[j] + ', ')
                    else:
                        msg += laggers[j]
                msg += (' lagaavat ' + name + 'ssä!')
            else:
                msg += (laggers[0] + ' lagaa ' + name + 'ssä!')
            irc.sendmsg(msg)            
        except:
            irc.sendmsg("Virhe! " + name + "n servuun ei saa yhteyttä!")
            
    def main(self, irc, line):
        f = filereader.read(settings.teamfile)
        if len(line) < 5:
            for i in range(len(f)):
                self.asklaggers(f[i].name, f[i].port, f[i].players, irc)
        else:
            for i in range(len(f)):
                if line[4] == f[i].name:
                    self.asklaggers(f[i].name, f[i].port, f[i].players, irc)
                        

command_dict[ ':!kukalagaa' ] = Kukalagaa()
