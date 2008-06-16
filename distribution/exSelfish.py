from economy import *
from grid import *
from full import *
from statistics import *
from experiments import *

SelfishGrid = gridMaker(Agent,10,10)
SelfishGridExperiment = experimentMaker(SelfishGrid)

SelfishFull = fullMaker(Agent,100)
SelfishFullExperiment =experimentMaker(SelfishFull)

if __name__ == '__main__' :
    experiment(SelfishGridExperiment,30,1000,resources(),'selfishgrid.csv')
    experiment(SelfishFullExperiment,30,1000,resources(),'selfishfull.csv')