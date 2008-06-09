import unittest
from random import choice

class OPTIMAESException(Exception) :
    def __init__(self,s='') : self.s = s
    def explain(self) : return s

class OPTIMAESPopulationDeadException(OPTIMAESException) : pass
class OPTIMAESHoodDeadException(OPTIMAESException) : pass

class Dummy :
    pass

def flatten(xs) :
    if xs.__class__ != list : return xs
    b=[]
    for x in xs:
        ys = flatten(x)
        if ys.__class__ != list :
            b.append(ys)
        else :
            b = b + ys
    return b

def gridMaker(nodeClass, crows=10, ccols=10) :

    class NetNode(nodeClass) :
        def __init__(self,net,id) :
            self.hood = []
            self.id = id
            self.network = net
            nodeClass.__init__(self)
        def getId(self) : return self.id
        def getHood(self) : return self.hood

    class Grid :

        def __init__(self, rows=crows,cols=ccols) :
            self.grid = [[None]*cols for x in range(rows)]
            self.rows = rows
            self.cols = cols
            counter = 0
            for y in range(rows) :
                for x in range(cols) :
                    self.grid[x][y] = NetNode(self,counter)
                    counter = counter + 1
                    
            # set up hood
            for y in range(rows):
                for x in range(cols) :
                    (self.grid[x][y]).hood = [
                        self.north(x,y), self.east(x,y),
                        self.south(x,y), self.west(x,y) ]

        def getNode(self,x,y) :
            return self.grid[x][y]
        def north(self,x,y) : return self.getNode(x,(y-1) % self.rows )
        def east(self,x,y) : return self.getNode((x+1) % self.cols,y)
        def south(self,x,y) : return self.getNode(x,(y+1) % self.rows )
        def west(self,x,y) : return self.getNode((x-1) % self.cols, y)        
        
        def getHood(self,x,y) :
            n = self.getNode(x,y)
            return n.hood

        def getAll(self) : return flatten(self.grid)
        def getAlive(self) : return [x for x in self.getAll() if x.isAlive()]

        def getRandom(self) : return choice(self.getAll())
        
        def getRandomLive(self) :
            try : return choice(self.getAlive())
            except : raise OPTIMAESPopulationDeadException()
                
        def printMap(self,printFn=None) :
            if printFn == None :
                for y in range(self.rows) :
                    for x in range(self.cols) :
                       print self.getNode(x,y).id,
                    print
                    
        def getRandomPair(self) :
            a = choice(self.getAll())
            b = choice(a.getHood())
            return(a,b)

        def allApply(self,fn) :
            for x in self.getAll() :
                fn(x)
        
        def allMap(self,fn) :
            r2=[]
            for r in self.grid :
                r2.append( [fn(x) for x in r] )
            return r2
        
        def addResources(self,recs) :
            for x in self.getAll() :
                for r in recs :
                    x.addResource(r[0],r[1],r[2])

        
    return Grid
            

class TestGridMaker(unittest.TestCase) :
    def test1(self) :
        class X :
            def __init__(self) :
                self.hello = "hello"
            def __str__(self) :
                return "X(%s)"%self.id
            
        GC = gridMaker(X,5,5)
        g = GC()
        g.printMap()
        print [x.id for x in g.getAll()]
        print g.getNode(0,3)
        self.assertEquals(g.getNode(0,3).id,15)
        self.assertEquals([x.id for x in g.getHood(0,3)],[10, 16, 20, 19])
        print [x.id for x in g.getRandomPair()]
        print [x.id for x in g.getRandomPair()]

        
if __name__ == '__main__' :
    unittest.main()
