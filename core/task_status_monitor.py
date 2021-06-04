import json


class TaskStatusMonitor(object):
    def __init__(self, simulation):
        self.simulation = simulation
        self.env = simulation.env
        self.event_file = simulation.event_file
        self.events = []
        self.mean_machine_power = 0
        self.total_energy_consume = 0



    def run(self):
        while not self.simulation.finished:
            state = {
                'timestamp': self.env.now,
                'cluster_state': self.simulation.cluster.state
            }
            power_sum = 0
            machine_state_list=self.simulation.cluster.state['machine_states']
            for machine_state in machine_state_list:
                power_sum += machine_state["power"]
            self.mean_machine_power = (power_sum/len(machine_state_list))
            self.total_energy_consume += power_sum
            # if self.total_energy_consume>1e7:
            #     print("too large")
            self.events.append(state)
            yield self.env.timeout(1)

        state = {
            'timestamp': self.env.now,
            'cluster_state': self.simulation.cluster.state
        }
        self.events.append(state)

        self.write_to_file()

    def write_to_file(self):
        with open(self.event_file, 'w') as f:
            json.dump(self.events, f, indent=4)
