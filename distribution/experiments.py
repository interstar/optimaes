from statistics import *

def oneRun(ExperimentClass,noSteps,resources) :
    c = Collector()
    acc = Accountant()
    def log(pop) : c.addLine([acc.countAlive(pop.getAll())])
    grid = ExperimentClass()
    grid.addResources(resources)
    grid.run(noSteps,log)
    return c.column(0)

def experiment(ExperimentClass,noRuns,noSteps,resources,fName) :
    c = Collector()
    for r in range(noRuns) :
        c.addLine(oneRun(ExperimentClass,noSteps,resources))
    c.writeAsFile(fName)


