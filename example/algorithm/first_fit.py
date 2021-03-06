from core.algorithm import Algorithm
from typing import Any


class FirstFitTaskalgorithm(Algorithm):
    def __call__(self, cluster, clock, cooling_equipment=None) -> (Any, Any, Any):
        machines = cluster.machines
        tasks = cluster.unfinished_tasks
        for task in tasks:
            for machine in machines:
                if machine.accommodate(task):
                    return machine, task, None
        return None, None, None
