import time
import numpy as np
from config import MachineConfig
from example.algorithm.first_fit import FirstFitTaskalgorithm
from example.utils.csv_reader import CSVReader
from example.utils.episode import Episode

np.random.seed(41)

# ************************ Parameters Setting Start ************************
machines_number = 5
jobs_csv = './jobs.csv'
machine_configs = [MachineConfig(64, 1, 1) for i in range(machines_number)]
csv_reader = CSVReader(jobs_csv)
jobs_configs=csv_reader.generate(0,1)
print("-----------------------------------------first_fit------------------------------------------")
algorithm = FirstFitTaskalgorithm()
episode = Episode(machine_configs, jobs_configs, algorithm, None)
tic = time.time()
episode.run()
print("simulation virtual time(s): ",episode.env.now)
print("running time(s): ",time.time() - tic)
total_energy_consume=0
for machine in episode.simulation.cluster.machines:
    total_energy_consume+=machine.energy_consume
print("total energy consume(kWh): ", total_energy_consume/60/60/1000)
