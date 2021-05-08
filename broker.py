from job import Job


class Broker(object):
    job_cls = Job

    def __init__(self, env, job_configs):
        self.env = env
        self.simulation = None
        self.cluster = None
        self.destroyed = False
        self.job_configs = job_configs

    def attach(self, simulation):
        self.simulation = simulation
        self.cluster = simulation.cluster

    def run(self):
        for job_config in self.job_configs:
            assert job_config.submit_time >= self.env.now
            # print("broker:","before yield")
            #(now+timeouttime,func)
            yield self.env.timeout(job_config.submit_time - self.env.now)
            # print("broker:","after yield")
            job = Broker.job_cls(self.env, job_config)
            # print('a job arrived at time %f' % self.env.now)
            self.cluster.add_job(job)
            # print("task len:", len(self.cluster.tasks_which_has_waiting_instance))
        self.destroyed = True
