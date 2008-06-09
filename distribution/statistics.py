
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
        
    def writeAsFile(self,fName) :
        file = open(fName,'w')
        for xs in self.table :
            file.write(','.join(['%s'%x for x in xs]))
            file.write('\n')
        file.close()
        
    def column(self,id) :
        return [x[id] for x in self.table]
    