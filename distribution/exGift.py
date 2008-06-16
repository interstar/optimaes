from economy import *
from grid import *
from full import *
from statistics import *
from experiments import *

class GiftAgent(Agent) :
            
    def findNeighbourWhoMostNeeds(self, rName) :
        # for resource named rName, identify the neighbour who most needs it,
        # assumes only called when SELF has a surplus in rName
        
        hood = self.getLiveNeighbours()
        neediestAgent = None
        neediestShortfall = 0 # the other agent is breaking even, don't need to donate
        transfer = 0
        for candidate in hood :
            need = candidate.getShortfall(rName)
            if need > neediestShortfall :
                neediestShortfall = need
                neediestAgent = candidate
                
        return neediestAgent
            

    def donateToNeediestNeighbours(self) :
        # for each resource, donate surplus to the neighbour who most needs it
        for rName in self.rrmaps.keys() :
            if self.getSurplus(rName) > 0 :
                neediest = self.findNeighbourWhoMostNeeds(rName)
                if neediest != None :
                    self.donateTo(neediest, rName, self.getSurplus(rName)) 
         
GiftGrid = gridMaker(GiftAgent,10,10)
GiftFull = fullMaker(GiftAgent,100)

class GiftGridExperiment(experimentMaker(GiftGrid)) :
    def match(self, a) :
        a.lifeStep()
        a.donateToNeediestNeighbours()
        a.testDies()

class GiftFullExperiment(experimentMaker(GiftFull)) :
    def match(self, a) :
        a.lifeStep()
        a.donateToNeediestNeighbours()
        a.testDies()
    

if __name__ == '__main__' :
    experiment(GiftGridExperiment,30,1000,resources(),'giftgrid.csv')
    experiment(GiftFullExperiment,30,1000,resources(),'giftfull.csv')
