from statistics import *

def resources() : return [['food',5,5],['drink',5,5],['love',5,5]]

def oneRun(ExperimentClass,noSteps,resources) :
    c = Collector()
    acc = Accountant()
    def log(pop) : c.addLine([acc.countAlive(pop.getAll())])
    print ExperimentClass().__class__
    exp = ExperimentClass()
    exp.addResources(resources)
    exp.run(noSteps,log)
    return c.column(0)

def experiment(ExperimentClass,noRuns,noSteps,resources,fName) :
    c = Collector()
    for r in range(noRuns) :
        c.addLine(oneRun(ExperimentClass,noSteps,resources))
    c = c.rotate()
    c.writeAsFile(fName,10)


def experimentMaker(baseClass,) :

    class Experiment(baseClass) :
        
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
    return Experiment