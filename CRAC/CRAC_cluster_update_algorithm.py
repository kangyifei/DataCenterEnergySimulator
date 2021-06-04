from core.algorithm import Algorithm
from keras.models import load_model
import numpy as np

model_path = "D:\code\CloudSimPy\core\CRAC\predict_server_inlet_1ConditionerOutletTemp+15ServerCpuUsage_15out_2.33.hdf5"

class ClusterUpdateAlgorithm(Algorithm):
    def __init__(self):
        self.call_num=0
        self.model=load_model(model_path)
    def __call__(self, cluster, clock, cooling_equip=None) -> None:
        # self.call_num+=1
        # print("ClusterUpdateAlgorithm",self.call_num)
        input = [cooling_equip.state_paraslist["inlet_temp"]]
        for machine in cluster.machines:
            input.append((1 - machine.cpu / machine.cpu_capacity) * 100)
        output = self.model.predict(np.array(input).reshape(1, 16))
        output = output.reshape(15, 1).tolist()
        i = 0
        for machine in cluster.machines:
            machine.inlet_temp = output[i][0]
            i += 1
