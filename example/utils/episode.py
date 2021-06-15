import simpy
from core.cluster import Cluster
from core.scheduler import Scheduler
from core.broker import Broker
from core.simulation import Simulation
from core.cooling_equipment import CoolingEquipment


class Episode(object):
    def __init__(self, machine_configs, task_configs, algorithm, event_file, is_DAG, cooling_equipment_config=None):
        self.env = simpy.Environment()
        cluster = Cluster()
        cluster.add_machines(machine_configs)
        task_broker = Broker(self.env, task_configs, is_DAG)
        scheduler = Scheduler(self.env, algorithm)
        cooling_equipment = None if cooling_equipment_config is None else CoolingEquipment(cooling_equipment_config)
        self.simulation = Simulation(self.env, cluster, task_broker, scheduler, event_file, cooling_equipment)

    def run(self):
        self.simulation.run()
        self.env.run()
