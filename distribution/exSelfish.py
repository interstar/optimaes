from economy import *
from grid import *
from statistics import *
from experiments import *

SelfishGrid = gridMaker(Agent,10,10)

class SelfishExperiment(SelfishGrid) :
    
    def match(self, a) :
        a.lifeStep()

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
    experiment(SelfishExperiment,10,400,[['food',5,5],['drink',5,5],['love',5,5]],'selfish1.csv')