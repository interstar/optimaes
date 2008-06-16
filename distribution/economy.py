import unittest
import random
from math import sqrt

class RRMap :

    """
    Resource Requirement Map
    This is the Agent's profile with respect to one particular resource
    'need' corresponds to the requirement for the resource
    'rgc' (Resource Getting Capacity) is the number of units of resource the agent produces each turn
    'rcr' (Resource Consumption Rate) is the number of units the agent consumes each turn
    'current' How much it has
    'totalConsumption' Remembers how much of the resource was consumed.
    """

    def __init__(self, name) :
        self.name = name
        self.rgc = 0.0 # resource getting capacity
        self.rcr = 0.0 # resource consumption rate
        self.current = 10.0
        self.type = "RRMap"
        self.totalConsumption = 0
        # total consumption counts the amount of the resource used throughout the history of this RRMap

    def randomize(self, rgcRange, rcrRange) :
        self.rgc = random.choice(range(rgcRange))
        self.rcr = random.choice(range(rcrRange))
        self.current = 0

    def __str__(self) :
        return "%s :   \t%s\t+%s\t -%s\ttotCon : %s " % (self.name, self.current, self.rgc, self.rcr, self.totalConsumption)

    def oneStep(self) :
        self.current = self.current + self.rgc
        self.current = self.current - self.rcr
        self.totalConsumption = self.totalConsumption + self.rcr

    def tooLow(self) :
        return ( self.current < -3)

    def getShortfall(self) :
        # if current is negative, we have shortfall,
        # shortfall is +ve if we really need and 
        # -ve if in surplus
        return -self.current

    def getSurplus(self) :
        # opposite of shortfall, what's the surplus of the agent
        # current, +ve when in surplus
        return self.current 

    def add(self, rrMap) :
        self.rgc = self.rgc + rrMap.rgc
        self.rcr = self.rcr + rrMap.rcr
        self.current = self.current + rrMap.current

    def subtract(self, rrMap) :
        self.rgc = self.rgc - rrMap.rgc
        self.rcr = self.rcr - rrMap.rcr
        self.current = self.current - rrMap.current

    def multiply(self, rrMap) :
        self.rgc = self.rgc * rrMap.rgc
        self.rcr = self.rcr * rrMap.rcr
        self.current = self.current * rrMap.current

    def divide(self,rrMap) :
        self.rgc = self.rgc / rrMap.rgc
        self.rcr = self.rcr / rrMap.rcr
        self.current = self.current / rrMap.current

    def sqrt(self) :
        self.rgc = sqrt(self.rgc)
        self.rcr = sqrt(self.rcr)
        self.current = sqrt(self.current)

    def resetToZero(self) :
        self.rgc = 0
        self.rcr = 0
        self.current = 0

    def set(self, rgc, rcr, current) :
        self.rgc = rgc
        self.rcr = rcr
        self.current = current   

    def divideAllBy(self, d) :
        self.rgc = self.rgc / d
        self.rcr = self.rcr / d
        self.current = self.current / d

    def spawnDeepCopy(self) :
        newMap = RRMap("copy of %s" % self.name)
        newMap.current = self.current
        newMap.rgc = self.rgc
        newMap.rcr = self.rcr
        return newMap

class Agent :

    """
    Base bass mixin for agents.
    Agents have a list of RRMaps, a live state, and possibly a node on the network
    """

    def __init__(self) :
        self.rrmaps = {} # hash of resource-maps indexed by name
        self.alive = True

        # indices based on current (wealth) and need (need)
        self.wealthIndex = 0
        self.needIndex = 0
        
    def __str__(self) :
        s = "Agent"
        if self.isAlive() : s=s+" (alive)"
        else: s=s+" (dead)"
        s = s +"\nResource Maps\n"
        s=s+'\n'.join(['%s'%r for r in self.rrmaps.values()])
        return s
    
    def isAlive(self) : return self.alive
    def die(self) : self.alive = False
    
    def addRRMap(self, rrmap) :
        self.rrmaps[rrmap.name] = rrmap

    def addResource(self, name, rgcRange, rcrRange) :
        r = RRMap(name)
        r.randomize(rgcRange, rcrRange)
        self.addRRMap(r)

    def getRRMaps(self) : return self.rrmaps
    
    def getRRMap(self, name) :
        return self.rrmaps[name]
    
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

    def getMaxNeed(self) :
        # returns the name and shortfall of the resource with greatest need
        maxShort = -1000000 # big negative number
        shortestName = ""
        for map in self.rrmaps.values() :
            if map.getShortfall() > maxShort :
                maxShort = map.getShortfall()
                shortestName = map.name
        return (shortestName, maxShort)

    def getMaxSurplus(self) :
        # returns the name and surplus of the resource with greatest need
        maxSurp = -1000000 # big number
        surplusName = ""
        for map in self.rrmaps.values() :
            if map.getSurplus() > maxSurp :
                maxSurp = map.getSurplus()
                surplusName = map.name
        return (surplusName, maxSurp)    
 
    def getSurplus(self, name) :
        # find the surplus for resource name
        return self.rrmaps[name].getSurplus()

    def getShortfall(self, name) :
        # find the shortfall for resource name
        # remember +ve if there is a shortfall ie. need > current
        return self.rrmaps[name].getShortfall()

    def receiveResource(self, name, donation) :
        self.rrmaps[name].current = self.rrmaps[name].current + donation

    def donateTo(self, other, rName, amount ) :
        # donate amount of resource rName to otherAgent
        other.receiveResource(rName, amount)
        self.receiveResource(rName, -1 * amount)

    def lifeStep(self) :
        for r in self.rrmaps.values() :
            r.oneStep()

    def testDies(self) :
        for r in self.rrmaps.values() :
            if r.tooLow() :
                self.die()
            
    def getLiveNeighbours(self) :
        return [x for x in self.getHood() if x.isAlive() ]

    def social(self) :
        pass # does nothing in default agent
    

class TestRRMap(unittest.TestCase) :
    def testOneMap(self) :
        r = RRMap("Food")

        r.rgc = 6   
        r.rcr = 5
        r.current = 10

        self.assertEquals(r.rgc,6)
        self.assertEquals(r.rcr,5)
        self.assertEquals(r.current,10)

        r.oneStep()
        self.assertEquals(r.current, 11)
        self.assertEquals(r.totalConsumption,5)

        r.oneStep()
        self.assertEquals(r.current,12)
        self.assertEquals(r
                          .totalConsumption,10)


        self.assertEquals(r.tooLow(),False)
        self.assertEquals(r.getSurplus(),12)
        self.assertEquals(r.getShortfall(),-12)

        r.current = -1
        self.assertTrue(r.tooLow())
        self.assertEquals(r.getShortfall(),1)
        self.assertEquals(r.getSurplus(),-1)
        
        
    def testAgent(self) :
        a = Agent()
        a.addResource("food",5,5)
        a.addResource("drink",5,5)
        a.addResource("air",5,5)
        a.addResource("love",5,5)
        self.assertEquals(len(a.getRRMaps()),4)
        
        print a
        a.lifeStep()
        print a
        a.oneStep()
        
if __name__ == '__main__':
    unittest.main()