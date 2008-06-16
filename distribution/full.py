from grid import *

# Fully interconnected population

    
def fullMaker(nodeClass,pSize) :
    
    class NetNode(nodeClass) :
        def __init__(self,net,id) :
            self.hood = []
            self.id = id
            self.network = net
            nodeClass.__init__(self)
        def getId(self) : return self.id
        def getHood(self) : return [x for x in self.network.getAll() if x is not self]
        
    class Full(WorldMixin) :

        def __init__(self, size=pSize) :
            self.pop = [NetNode(self,x) for x in range(size)]            
            self.size = size
                        
        def getNode(self,i) :
            return self.pop[i]
        
        def getHood(self,i) :
            n = self.getNode(i)
            return n.hood
    
        def getAll(self) : return self.pop       
        
    return Full
        
        