class Value:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit


class CFDSolution:
    def __init__(self):
        self.entityMap = {}
        self.transient=False
    def isTransient(self):
        return self.transient
    def setTransient(self,transient):
        self.transient=transient
    def setAttr(self, entityType, name, attribute, value, unit):
        if self.entityMap.get(entityType) is None:
            self.entityMap[entityType] = {}
        if self.entityMap[entityType].get(name) is None:
            self.entityMap[entityType][name] = {}
        self.entityMap[entityType][name][attribute] = Value(value, unit)

# if __name__=="__main__":
#     sol=CFDSolution()
#     sol.setAttr("ACU", "ACU01", "CoolantFlowRate", "0.00145", "m^3/s")
#     sol.setAttr("ACU", "ACU02", "CoolantFlowRate", "0.00145", "m^3/s")
#     sol.setAttr("ACU", "ACU02", "CoolantFlowRate2", "0.00145", "m^3/s")