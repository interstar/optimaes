
import unittest

class Accountant :

    def alive(self,population) :
        return [x for x in population if x.isAlive()]
    
    def countAlive(self, population) :
        return len(self.alive(population))

    def showAlive(self, population) :
        return '\n'.join(['%s: %s'%(a.id,a)
                          for a in self.alive(population)])
    


class Collector :
    
    def __init__(self) :
        self.table = []
    
    def addLine(self,line) :
        self.table.append(line)
        
    def writeAsFile(self,fName,sample=1) :
        file = open(fName,'w')
        count = 0
        for xs in self.table :
            count = count+1
            if count % sample == 0 :
                file.write(','.join(['%s'%x for x in xs]))
                file.write('\n')
        file.close()
        
    def column(self,id) :
        return [x[id] for x in self.table]
    
    def rotate(self) :
        new = Collector()
        for x in range(len(self.table[0])) :
            new.addLine(self.column(x))
        return new

if __name__ == '__main__' :
    c = Collector()
    c.addLine([1,2,3])
    c.addLine([4,5,6])
    c.addLine([7,8,9])
    d = c.rotate()
    print d.table