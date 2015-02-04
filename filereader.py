# -*- coding: utf-8 -*-

class Gamedata:

    def __init__(self, name, port, players):
        self.name = name
        self.port = port
        self.players = players


def read(file):
    names = []
    ports = []
    players = []
    with open(file, 'r') as f:
        newgame = True
        gamenum = 0
        for line in f:
            if newgame and line.strip() != "":
                newgame = False
                data = line.split(',')
                names.append(data[0])
                ports.append(int(data[1]))
                players.append({})
            elif line.strip() == "":
                if not newgame:
                    gamenum += 1
                newgame = True
            else:
                data = line.split(',')
                players[gamenum][data[0].strip()] = data[1].strip()
    games = []
    for i in range(gamenum + 1):
        games.append(Gamedata(names[i], ports[i], players[i]))
    
    return games
        
        