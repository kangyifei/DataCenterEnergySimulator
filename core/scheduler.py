from core.cooling_equipment import CoolingEquipment
from core.algorithm import Algorithm


class Scheduler(object):
    def __init__(self, env, scheduler_algorithm: Algorithm):
        self.env = env
        self.scheduler_algorithm = scheduler_algorithm
        self.simulation = None
        self.cluster = None
        self.destroyed = False
        self.task_scheduled_num = 0
        self.task_finished_num = 0

    def attach(self, simulation):
        self.simulation = simulation
        self.cluster = simulation.cluster
        self.cooling_equipment = simulation.cooling_equipment

    def job_added_schedule(self):
        while True:
            machine, task, cooling_paramslist = self.scheduler_algorithm(self.cluster, self.env.now,
                                                                         self.cooling_equipment)
            if machine is None:
                if task is None:
                    break
                else:
                    continue
            else:
                self.task_scheduled_num += 1
                task.start_task_instance(machine)
        if self.cooling_equipment is not None:
            if cooling_paramslist is not None:
                self.cooling_equipment.control(cooling_paramslist)
                self.cooling_equipment.update_self(self.env.now)
                self.cooling_equipment.update_cluster()

    def job_finished_schedule(self):
        self.task_finished_num += 1
        machine, task, cooling_paramslist = self.scheduler_algorithm(self.cluster, self.env.now, self.cooling_equipment)
        if self.cooling_equipment is not None:
            if cooling_paramslist is not None:
                self.cooling_equipment.control(cooling_paramslist)
                self.cooling_equipment.update_self(self.env.now)
                self.cooling_equipment.update_cluster()

    def run(self):
        while not self.simulation.finished:
            if len(self.cluster.tasks_which_has_waiting_instance) == 0:
                value = yield self.simulation.job_event
                if value == "add":
                    self.job_added_schedule()
                else:
                    self.job_finished_schedule()
            else:
                value = (yield self.simulation.job_event | self.env.timeout(1, value="timeout")).values()
                value = next(value)
                if value == "add":
                    self.job_added_schedule()
                elif value == "finished":
                    self.job_finished_schedule()
                else:
                    self.job_added_schedule()
        self.destroyed = True
