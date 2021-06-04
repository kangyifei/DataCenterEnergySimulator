from core.algorithm import Algorithm


class ControlAlgorithm(Algorithm):
    def __call__(self, cluster, clock, cooling_equip=None):
        return {}


class ClusterUpdateAlgorithm(Algorithm):
    def __call__(self, cluster, clock, cooling_equip=None) -> None:
        pass
