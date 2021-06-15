import time
import numpy as np
from core.config import MachineConfig, CoolingEquipmentConfig
from SixSigmaDC.Room import Room
from example.algorithm.first_fit_with_CRAC import FirstFitTaskWithCRACalgorithm
from example.utils.csv_reader import CSVReader
from example.utils.episode import Episode

np.random.seed(41)

# ************************ Parameters Setting Start ************************
machines_number = 50
jobs_csv = './jobs.csv'
sixSigma_base_path= "./BigServer/1-/SolverExchange"
machine_configs = [MachineConfig(64, 1, 1) for i in range(machines_number)]
cooling_eq= Room(sixSigma_base_path)
csv_reader = CSVReader(jobs_csv)
jobs_configs = csv_reader.generate(0, 20)
print("-----------------------------------------first_fit------------------------------------------")
algorithm = FirstFitTaskWithCRACalgorithm()
episode = Episode(machine_configs, jobs_configs, algorithm, None, is_DAG=False,
                  cooling_equipment=cooling_eq)
tic = time.time()
episode.run()
print("cluster finished task num: ", episode.simulation.cluster.cluster_task_finished_num)
print("simulation virtual time(s): ", episode.env.now)
print("running time(s): ", time.time() - tic)
total_energy_consume = 0
for machine in episode.simulation.cluster.machines:
    total_energy_consume += machine.energy_consume
total_energy_consume += episode.simulation.cooling_equipment.energy_consume
print("total energy consume(kWh): ", total_energy_consume / 60 / 60 / 1000)
