from economy import *
from grid import *
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

class GiftExperiment(GiftGrid) :
        
    def match(self, a) :
        a.lifeStep()
        a.donateToNeediestNeighbours()
        
        a.testDies()

    def run(self,noSteps,log=lambda x:x) :
        for step in range(noSteps) :            
            try :
                a = self.getRandomLive()
            except OPTIMAESPopulationDeadException, e :
                return step # population dead after this number of steps
            self.match(a)
            log(self)
        return step        


if __name__ == '__main__' :
    experiment(GiftExperiment,10,400,[['food',5,5],['drink',5,5],['love',5,5]],'gift1.csv')
