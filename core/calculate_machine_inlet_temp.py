from abc import ABC, abstractmethod


class CalculateMachineInletTemp(ABC):
    @abstractmethod
    def __call__(self, cluster, cooling_equip):
        pass
