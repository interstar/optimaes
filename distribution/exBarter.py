from economy import *
from grid import *
from full import *
from statistics import *
from experiments import *

class BarterAgent(Agent) :


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
            if other.doYouWant(myNeed, mnAmount, rName, self.getSurplus(rName)) :
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
BarterFull = fullMaker(BarterAgent,100)

class BarterGridExperiment(experimentMaker(BarterGrid)) :        
    def match(self, a) :
        a.lifeStep()
        a.barterForAllNeeds()        
        a.testDies()
        
class BarterFullExperiment(experimentMaker(BarterFull)) :
    def match(self, a) :
        a.lifeStep()
        a.barterForAllNeeds()        
        a.testDies()
    


if __name__ == '__main__' :
    experiment(BarterGridExperiment,30,1000,resources(),'bartergrid.csv')
    experiment(BarterFullExperiment,30,1000,resources(),'barterfull.csv')
