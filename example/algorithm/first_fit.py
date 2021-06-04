from core.algorithm import Algorithm
from typing import Any

class FirstFitTaskalgorithm(Algorithm):
    def __call__(self, cluster, clock,cooling_equipment=None)->(Any,Any,Any):
        machines = cluster.machines
        tasks = cluster.unfinished_tasks
        candidate_task = None
        candidate_machine = None
        found=False
        for task in tasks:
            for machine in machines:
                if machine.accommodate(task):
                    candidate_machine = machine
                    candidate_task = task
                    found=True
                    break
            if found:
                break
        return candidate_machine, candidate_task,None