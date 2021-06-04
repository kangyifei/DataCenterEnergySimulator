from core.config import CoolingEquipmentConfig
import importlib
import importlib.util

class CoolingEquipment(object):

    def __init__(self, coolingconfig: CoolingEquipmentConfig):
        self.state_paraslist = {}
        for paramkey in coolingconfig.state_paramslist:
            self.state_paraslist[paramkey] = coolingconfig.state_paramslist[paramkey]["now"]
        self.control_paramslist = {}
        for paramkey in coolingconfig.control_paramslist:
            self.control_paramslist[paramkey] = coolingconfig.control_paramslist[paramkey]["now"]
        self.machines = None
        self.simulation = None
        self.cluster = None
        control_module = importlib.import_module(coolingconfig.control_algorithm)
        ca = control_module.ControlAlgorithm()
        self.control_algorithm = ca
        cluster_module = importlib.import_module(coolingconfig.cluster_update_algorithm)
        cm = cluster_module.ClusterUpdateAlgorithm()
        self.cluster_update_algorithm = cm

    def update_self(self):
        new_state_paramslist = self.control_algorithm(self.cluster, None, self)
        for paramkey in self.state_paraslist:
            if paramkey in new_state_paramslist:
                self.state_paraslist[paramkey] = new_state_paramslist[paramkey]

    def control(self, control_paramslist):
        for paramkey in control_paramslist:
            if paramkey in self.control_paramslist:
                self.control_paramslist[paramkey] = control_paramslist[paramkey]

    def update_cluster(self):
        self.cluster_update_algorithm(self.cluster, None, self)

    def attach(self, simulation):
        self.simulation = simulation
        self.cluster = simulation.cluster
        self.machines = self.cluster.machines

    # def cal_machines_temp(self):
    #     model_path = "CRAC/predict_server_inlet_1ConditionerOutletTemp+15ServerCpuUsage_15out_2.33.hdf5"
    #     model = load_model(model_path)
    #     input = [self.get_setting_temp()]
    #     for machine in self.simulation.cluster.machines:
    #         input.append((1 - machine.cpu / machine.cpu_capacity) * 100)
    #     output = model.predict(np.array(input).reshape(1, 16))
    #     output = output.reshape(15, 1).tolist()
    #     return output
    #
    # def cal_self_temp(self):
    #     model_path = "CRAC/predict_condition_inlet_15ServerInletTempin_1out_0.15.hdf5"
    #     model = load_model(model_path)
    #     input = []
    #     for machine in self.simulation.cluster.machines:
    #         input.append(machine.inlet_temp)
    #     output = model.predict(np.array(input).reshape(1, 15))
    #     return output[0]
    #
    # def __cal_machines_inlet_temp(self):
    #     machines_temp = self.cal_machines_temp()
    #     for i in range(len(self.machines)):
    #         self.machines[i].inlet_temp = machines_temp[i]
    #
    # def run(self):
    #     while not self.simulation.finished:
    #         yield self.simulation.job_added_event | self.simulation.job_finished_event
    #         self.inlet_temp = self.cal_self_temp()
    #         self.__cal_machines_inlet_temp()
    #
    # @property
    # def state(self):
    #     return {
    #         "setting_temp": self.setting_temp,
    #         "inlet_temp": self.inlet_temp
    #     }
