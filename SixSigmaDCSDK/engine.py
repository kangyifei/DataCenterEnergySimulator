import os
from SixSigmaDCSDK.CFDSolution import CFDSolution
import time
class Engine:
    def __init__(self):
        self.solution=CFDSolution()
        self.changedSolution=CFDSolution()
    def readCFDOutFile(self,filepath):
        if not os.path.exists(filepath):
            time.sleep(1)
            return False
        findEnd = False
        with open(filepath,"r") as f:
            firstLine=f.readline()
            if not firstLine=="<<,START,CSV,VER00,>>\n":
                time.sleep(1)
                return False
            titleLine=f.readline()
            timeEqual=False
            while True:
                line=f.readline()
                if line=="<<,END,CSV,VER00,>>\n":
                    findEnd=True
                    break
                lineSplited=line.split(",")
                if lineSplited[4].find("\n")!=-1:
                    lineSplited[4]=lineSplited[4].replace("\n","")
                if lineSplited[0]=="<<Control>>":
                    if lineSplited[1]=="<<Solution>>":
                        # TOD0:valiate out csv
                        if lineSplited[2]=="Time":
                            self.solution.setTransient(True)
                            try:
                                iter = self.solution.entityMap["<<Control>>"]["<<Solution>>"]["Time"]
                            except KeyError:
                                print("first init")
                                pass
                            else:
                                iterValue = iter.value
                                if int(iterValue) > int(lineSplited[3]):
                                    print("need to wait SixSigmaDC update")
                                    time.sleep(1)
                                    return False
                                elif int(iterValue) == int(lineSplited[3]):
                                    timeEqual=True
                        if (not self.solution.isTransient()) or timeEqual:
                            if lineSplited[2]=="Iteration":
                                try:
                                    iter=self.solution.entityMap["<<Control>>"]["<<Solution>>"]["Iteration"]
                                except KeyError:
                                    pass
                                else:
                                    iterValue=iter.value
                                    if int(iterValue)>=int(lineSplited[3]):
                                        return False
                        self.solution.setAttr(lineSplited[0],lineSplited[1],lineSplited[2],lineSplited[3],lineSplited[4])

                else:
                    self.solution.setAttr(lineSplited[0],lineSplited[1],lineSplited[2],lineSplited[3],lineSplited[4])
        if not findEnd:
            return False
        return True
    def setSolutionAttr(self,entityType,name,attr,value,unit):
        self.changedSolution.setAttr(entityType,name,attr,value,unit)
    def getSolutionAttr(self,entityType,name,attr):
        try:
            val=self.solution.entityMap[entityType][name][attr]
        except:
            return None
        return val
    def writeCFDInFile(self,filePath):
        while True:
            try:
                with open(filePath,"w+") as f:
                    f.write("<<,START,CSV,VER00,>>\n")
                    f.write("EntityType,Name,Attribute,Value,Unit\n")
                    for entityType in sorted(self.solution.entityMap.keys()):
                        for name in self.solution.entityMap[entityType].keys():
                            for attr in self.solution.entityMap[entityType][name].keys():
                                line=entityType+","+name+","+attr+","\
                                     +self.solution.entityMap[entityType][name][attr].value+","\
                                     +self.solution.entityMap[entityType][name][attr].unit+"\n"
                                f.write(line)
                    f.write("<<,END,CSV,VER00,>>\n")
                    break
            except PermissionError:
                pass

if __name__=="__main__":
    eng=Engine()
    eng.readCFDOutFile("D:\code\CloudSimPy\playground\\Non_DAG_with_Energy\\5Server\Baseline\SolverExchange\out.csv")
    eng.readCFDOutFile("D:\code\CloudSimPy\playground\\Non_DAG_with_Energy\\5Server\Baseline\SolverExchange\out.csv")
    eng.writeCFDInFile("in.csv")
    print("a")