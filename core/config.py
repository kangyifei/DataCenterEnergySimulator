from typing import List
import json


class TaskInstanceConfig(object):
    def __init__(self, task_config):
        self.cpu = task_config.cpu
        self.memory = task_config.memory
        self.disk = task_config.disk
        self.duration = task_config.duration


class TaskConfig(object):
    def __init__(self, task_index, instances_number, cpu, memory, disk, duration, parent_indices=None):
        self.task_index = task_index
        self.instances_number = instances_number
        self.cpu = cpu
        self.memory = memory
        self.disk = disk
        self.duration = duration
        self.parent_indices = parent_indices


class JobConfig(object):
    def __init__(self, idx, submit_time, task_configs):
        self.submit_time = submit_time
        self.task_configs = task_configs
        self.id = idx


class MachineConfig(object):
    idx = 0

    def __init__(self, cpu_capacity, memory_capacity, disk_capacity, cpu=None, memory=None, disk=None,
                 calculate_machine_inlet_temp=None):
        self.cpu_capacity = cpu_capacity
        self.memory_capacity = memory_capacity
        self.disk_capacity = disk_capacity

        self.cpu = cpu_capacity if cpu is None else cpu
        self.memory = memory_capacity if memory is None else memory
        self.disk = disk_capacity if disk is None else disk
        self.cal_inlet_temp = calculate_machine_inlet_temp
        self.id = MachineConfig.idx
        MachineConfig.idx += 1


class CoolingEquipmentConfig(object):
    idx = 0

    def __init__(self, jsonFilePath):
        with open(jsonFilePath, "r") as f:
            j = json.load(f)
        self.name = j["name"]
        self.state_paramslist = j["params"]["state"]
        self.control_paramslist = j["params"]["control"]
        self.control_algorithm = j["params"]["control_algorithm"]
        self.cluster_update_algorithm = j["params"]["cluster_update_algorithm"]
        self.id = CoolingEquipmentConfig.idx
        CoolingEquipmentConfig.idx += 1
