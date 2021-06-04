from core.job import Job


class Broker(object):
    def __init__(self, env, job_configs,is_DAG):
        self.env = env
        self.simulation = None
        self.cluster = None
        self.destroyed = False
        self.job_configs = job_configs
        self.is_DAG=is_DAG
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
            job = Job(self.env, job_config)
            # print('a job arrived at time %f' % self.env.now)
            self.cluster.add_job(job,self.is_DAG)
            # print("task len:", len(self.cluster.tasks_which_has_waiting_instance))
        self.destroyed = True
