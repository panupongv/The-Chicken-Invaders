import pickle

from constants import *

class ScoreProcessor(object):
    def __init__ (self):
        self.scores = self.getScores()
        self.colors = self.getColors()
        
    def getScores(self):
        try:
            inFile = open("Resources\\Documents\\highscore.dat","rb")
            self.scores = pickle.load(inFile)
            inFile.close()
        except IOError:
            return dict()
        return self.scores

    def getColors(self):
        try:
            inFile = open("Resources\\Documents\\highscore.dat","rb")
            pickle.load(inFile)
            self.colors = pickle.load(inFile)
            inFile.close()
        except IOError:
            return dict()
        return self.colors
        
    def writeScore(self, score, name, playerClass):
        if playerClass == 1:
            tempCol = RED
        elif playerClass == 2:
            tempCol = GREEN
        elif playerClass == 3:
            tempCol = YELLOW
        elif playerClass == 4:
            tempCol = GREY
        else:
            tempCol = WHITE
        while score in self.scores:
            score += 1
        self.scores[score] = name
        self.colors[score] = tempCol
        outFile = open("Resources\\Documents\\highscore.dat","wb")
        pickle.dump(self.scores, outFile)
        pickle.dump(self.colors, outFile)
        outFile.close()
