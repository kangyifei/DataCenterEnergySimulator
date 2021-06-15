from core.algorithm import Algorithm
from core.cooling_equipment import CoolingEquipment
from keras.models import load_model
import numpy as np

model_path = "../CRAC/predict_condition_inlet_15ServerInletTempin_1out_0.15.hdf5"


class ControlAlgorithm(Algorithm):
    def __init__(self):
        self.model = load_model(model_path)

    def __call__(self, cluster, clock, cooling_equip: CoolingEquipment = None):
        input = []
        for machine in cluster.machines:
            input.append(machine.inlet_temp)
        output = self.model.predict(np.array(input).reshape(1, 15))
        return {"inlet_temp": output.tolist()[0][0]}
