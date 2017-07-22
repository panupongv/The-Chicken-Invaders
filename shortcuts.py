import Player
import Items
import Game

class PlayerDict(object):
    def __init__(self):
        self.players = {1:Player.Ship1,
                        2:Player.Ship2,
                        3:Player.Ship3,
                        4:Player.Ship4}
    def get(self, num, *group):
        return self.players.get(num)(*group)

class ItemDict(object):
    def __init__(self):
        self.items = {1:Items.PowerUp1,
                      2:Items.PowerUp2,
                      3:Items.PowerUp3,
                      4:Items.PowerUp4,
                      5:Items.PowerUp5}
    def get(self, num, *group):
        return self.items.get(num)(*group)

class GameConstructor(object):
    def __init__(self):
        self.chickenPerLine =    {1:2,     2:3,    3:4,    4:4,    5:4}
        self.chickenNum =        {1:15,    2:25,   3:30,   4:40,   5:50}
        self.chickenFrequency =  {1:300,   2:300,  3:300,  4:300,  5:300}
        self.bigChickNum =       {1:0 ,    2:3,    3:4,    4:7,    5:12}
        self.bigChickFrequency = {1:1500,  2:1500, 3:1500, 4:1000, 5:750}
        self.meteorNum =         {1:0 ,    2:1,    3:1,    4:1,    5:1}
        self.boxNum =            {1:2 ,    2:2,    3:2,    4:3,    5:3}
        self.bomberLeft =        {1:-100,  2:-100, 3:-600, 4:-500, 5:-400}
        self.bomberRight =       {1:-50,   2:-50,  3:1200, 4:1100, 5:1000}
        self.picName = {1:"Resources\\Generals\\level1.jpg",
                        2:"Resources\\Generals\\level2.jpg",
                        3:"Resources\\Generals\\level3.jpg",
                        4:"Resources\\Generals\\level4.jpg",
                        5:"Resources\\Generals\\level5.jpg"}
    def get(self, num, screen, playerClass, mutables):
        return Game.Game(screen, playerClass, mutables,
                         self.chickenPerLine[num], self.chickenNum[num], self.chickenFrequency[num],
                         self.bigChickNum[num], self.bigChickFrequency[num],
                         self.meteorNum[num], self.boxNum[num],
                         self.bomberLeft[num], self.bomberRight[num],
                         self.picName[num])


        
        
