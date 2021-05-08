from task_status_monitor import TaskStatusMonitor


class Simulation(object):
    def __init__(self, env, cluster, task_broker, scheduler, event_file, cooling_equipment=None):
        self.env = env
        self.cluster = cluster
        self.task_broker = task_broker
        self.scheduler = scheduler
        self.event_file = event_file
        self.cooling_equipment = cooling_equipment
        self.task_monitor=TaskStatusMonitor(self)
        self.monitor = []
        self.job_event = env.event()
        # self.job_finished_event = env.event()
        if event_file is not None:
            self.monitor.append(self.task_monitor)
        if cooling_equipment is not None:
            self.cooling_equipment.attach(self)
        self.cluster.attach(self)
        self.cluster.attach_monitor(self.task_monitor)
        self.task_broker.attach(self)
        self.scheduler.attach(self)

    def run(self):
        # Starting monitor process before task_broker process
        # and scheduler process is necessary for log records integrity.
        for mon in self.monitor:
            self.env.process(mon.run())
        self.env.process(self.task_broker.run())
        self.env.process(self.scheduler.run())

    @property
    def finished(self):
        return self.task_broker.destroyed \
               and len(self.cluster.unfinished_jobs) == 0
