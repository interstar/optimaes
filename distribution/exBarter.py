from economy import *
from grid import *
from statistics import *
from experiments import *

class BarterAgent(Agent) :

    def getListOfNeeds(self) :
        l = []
        for rrmap in self.rrmaps.values() :
            if rrmap.getShortfall() > 0 :
                l.append(rrmap.name)
        return l

    def getListOfSurpluses(self) :
        l = []
        for rrmap in self.rrmaps.values() :
            if rrmap.getSurplus() > 0 :
                l.append(rrmap.name)
        return l


    # receive an offer, decide whether to take it
    def doYouWant(self, otherWants, owAmount, otherHas, ohAmount) :
        if self.getSurplus(otherWants) > owAmount and self.getShortfall(otherHas) < ohAmount and self.getShortfall(otherHas) > 0 :
            return True # accept barter offer
        else :
            return False # reject barter offer

    # do the barter
    def barter(self, otherWants, owAmount, otherHas, ohAmount, other) :
        self.donateTo(other,otherWants,owAmount)
        other.donateTo(self,otherHas,ohAmount)

    # given a particular need, find something OTHER wants
    # note OTHER is offering all it's surplus here. Could be improved
    def findSomethingOtherWants(self, myNeed, mnAmount, other) :
        trade = None        
        for rName in self.getListOfSurpluses() :
            if other.doYouWant(myNeed, mnAmount, rName, self.getSurplus(rName)) == 1 :
                trade = rName
                break
        return trade

    # for a particular need, find a neighbour willing to barter for it
    def findBarterPartnerAndBarterForNeed(self, myNeed, mnAmount) :
        hood = self.getLiveNeighbours()
        for candidate in hood :
            trade =  self.findSomethingOtherWants(myNeed, mnAmount, candidate)
            if trade != None :
                # found a valid barter for this need, do it

                # don't trade whole of surplus, only what OTHER needs
                # so use  candidate.getShortfall(trade)
                self.barter(trade, candidate.getShortfall(trade), myNeed, mnAmount, candidate)
                break


    # for each need find a partner and barter
    def barterForAllNeeds(self) :
        needs = self.getListOfNeeds()
        for need in needs :
            self.findBarterPartnerAndBarterForNeed(need, self.getShortfall(need))
            

BarterGrid = gridMaker(BarterAgent,10,10)

class BarterExperiment(BarterGrid) :
        
    def match(self, a) :
        a.lifeStep()
        a.barterForAllNeeds()        
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
    experiment(BarterExperiment,10,1000,[['food',5,5],['drink',5,5],['love',5,5]],'barter1.csv')
