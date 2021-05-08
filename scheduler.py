from core.cooling_equipment import CoolingEquipment
from core.algorithm import Algorithm


class Scheduler(object):
    def __init__(self, env, scheduler_algorithm: Algorithm, cooling_equipment: CoolingEquipment = None):
        self.env = env
        self.scheduler_algorithm = scheduler_algorithm
        self.cooling_equipment = cooling_equipment
        self.simulation = None
        self.cluster = None
        self.destroyed = False
        self.valid_pairs = {}
        self.task_scheduled_num = 0
        self.task_finished_num = 0

    def attach(self, simulation):
        self.simulation = simulation
        self.cluster = simulation.cluster

    def job_added_schedule(self):
        while True:
            machine, task, cooling_paramslist = self.scheduler_algorithm(self.cluster,
                                                                         self.env.now,
                                                                         self.cooling_equipment)
            # print("task len:", len(self.cluster.tasks_which_has_waiting_instance))
            if machine is None or task is None:
                # print("waiting task all gone")
                break
            else:
                self.task_scheduled_num += 1
                task.start_task_instance(machine)
                # print("new task started")
        if self.cooling_equipment is not None:
            if cooling_paramslist is not None:
                self.cooling_equipment.control(cooling_paramslist)
                self.cooling_equipment.update_self()
                self.cooling_equipment.update_cluster()

    def job_finished_schedule(self):
        self. task_finished_num += 1
        machine, task, cooling_paramslist = self.scheduler_algorithm(self.cluster,
                                                                     self.env.now,
                                                                     self.cooling_equipment)
        if self.cooling_equipment is not None:
            if cooling_paramslist is not None:
                self.cooling_equipment.control(cooling_paramslist)
                self.cooling_equipment.update_self()
                self.cooling_equipment.update_cluster()

    def run2(self):
        while not self.simulation.finished:
            if not self.simulation.task_broker.destroyed:
                value = yield self.simulation.job_event
                if value == "add":
                    # print("job added")
                    self.job_added_schedule()
                else:
                    # print("job finished1")
                    self.job_finished_schedule()
            else:
                # print("scheduler:", "before yield2")
                value = (yield self.simulation.job_event | self.env.timeout(1)).values()
                value = next(value)
                # print(value)
                if value == "finished":
                    # print("job finished2")
                    self.job_finished_schedule()
                else:
                    # print("job added")
                    self.job_added_schedule()
        self.destroyed = True
        print("sched num: ", self.task_scheduled_num)
        print("finished num: ", self.task_finished_num)

    # def run(self):
    #     while not self.simulation.finished:
    #         if len(self.cluster.tasks_which_has_waiting_instance) == 0:
    #             value = yield self.simulation.job_event
    #             if value == "add":
    #                 # print("job added")
    #                 self.job_added_schedule()
    #             else:
    #                 # print("job finished1")
    #                 self.job_finished_schedule()
    #         else:
    #             yield self.env.timeout(1)
    #             self.job_added_schedule()
    #
    #     self.destroyed = True
    #     print("sched num: ", self.task_scheduled_num)
    #     print("finished num: ", self.task_finished_num)
    def run(self):
        while not self.simulation.finished:
            yield self.env.timeout(1)
            self.job_added_schedule()
        self.destroyed = True
        print("sched num: ", self.task_scheduled_num)
        print("finished num: ", self.task_finished_num)
    def run3(self):
        while not self.simulation.finished:
            yield self.env.timeout(1)
            self.job_added_schedule()
        self.destroyed = True
        print("sched num: ", self.task_scheduled_num)
        print("finished num: ", self.task_finished_num)
