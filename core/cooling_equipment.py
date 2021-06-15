from core.config import CoolingEquipmentConfig
import importlib
import importlib.util


class CoolingEquipment(object):

    def __init__(self, coolingconfig: CoolingEquipmentConfig):
        self.state_paraslist = coolingconfig.state_paramslist
        # for paramkey in coolingconfig.state_paramslist:
        #     self.state_paraslist[paramkey]={}
        #     self.state_paraslist[paramkey]["now"]=coolingconfig.state_paramslist[paramkey]["now"]
        #     self.state_paraslist[paramkey]["low"] = coolingconfig.state_paramslist[paramkey]["low"]
        #     self.state_paraslist[paramkey]["high"] = coolingconfig.state_paramslist[paramkey]["high"]
        self.control_paramslist = coolingconfig.control_paramslist
        # for paramkey in coolingconfig.control_paramslist:
        #     self.control_paramslist[paramkey] = {}
        #     self.control_paramslist[paramkey]["now"] = coolingconfig.control_paramslist[paramkey]["now"]
        #     self.control_paramslist[paramkey]["low"] = coolingconfig.control_paramslist[paramkey]["low"]
        #     self.control_paramslist[paramkey]["high"] = coolingconfig.control_paramslist[paramkey]["high"]
        self.machines = None
        self.simulation = None
        self.cluster = None
        self.energy_consume = 0
        self.last_update_time = 0
        control_module = importlib.import_module(coolingconfig.control_algorithm)
        self.control_algorithm = control_module.ControlAlgorithm()
        cluster_module = importlib.import_module(coolingconfig.cluster_update_algorithm)
        self.cluster_update_algorithm = cluster_module.ClusterUpdateAlgorithm()
        energy_module = importlib.import_module(coolingconfig.power_algorithm)
        self.power_algorithm = energy_module.PowerAlgorithm()

    def update_self(self, now):
        new_state_paramslist = self.control_algorithm(self.cluster, None, self)
        for paramkey in self.state_paraslist:
            if paramkey in new_state_paramslist:
                self.state_paraslist[paramkey]["now"] = new_state_paramslist[paramkey]
                if self.state_paraslist[paramkey]["now"] > self.state_paraslist[paramkey]["high"]:
                    self.state_paraslist[paramkey]["now"] = self.state_paraslist[paramkey]["high"]
                elif self.state_paraslist[paramkey]["now"] < self.state_paraslist[paramkey]["low"]:
                    self.state_paraslist[paramkey]["now"] = self.state_paraslist[paramkey]["high"]
        self.energy_consume += ((now - self.last_update_time) * self.power_algorithm(self.cluster, now, self))
        self.last_update_time = now

    def control(self, control_paramslist):
        for paramkey in control_paramslist:
            if paramkey in self.control_paramslist:
                self.control_paramslist[paramkey]["now"] = control_paramslist[paramkey]
                if self.control_paramslist[paramkey]["now"] > self.control_paramslist[paramkey]["high"]:
                    self.control_paramslist[paramkey]["now"] = self.control_paramslist[paramkey]["high"]
                elif self.control_paramslist[paramkey]["now"] < self.control_paramslist[paramkey]["low"]:
                    self.control_paramslist[paramkey]["now"] = self.control_paramslist[paramkey]["high"]

    def update_cluster(self):
        self.cluster_update_algorithm(self.cluster, None, self)

    def attach(self, simulation):
        self.simulation = simulation
        self.cluster = simulation.cluster
        self.machines = self.cluster.machines
