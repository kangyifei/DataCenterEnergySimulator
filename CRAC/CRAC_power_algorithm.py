from core.algorithm import Algorithm
from core.cooling_equipment import CoolingEquipment


class PowerAlgorithm(Algorithm):
    def __init__(self):
        pass

    def __call__(self, cluster, clock, cooling_equip: CoolingEquipment = None):
        power = (cooling_equip.state_paraslist["inlet_temp"]["now"] - cooling_equip.control_paramslist["set_temp"][
            "now"]) * 100
        if power < 0:
            power = 0
        return power
