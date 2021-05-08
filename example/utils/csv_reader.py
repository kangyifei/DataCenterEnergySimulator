from operator import attrgetter
import pandas as pd
import numpy as np

from core.job import JobConfig, TaskConfig


class CSVReader(object):
    def __init__(self, filename):
        self.filename = filename
        df = pd.read_csv(self.filename)

        df.task_id = df.task_id.astype(dtype=int)
        df.job_id = df.job_id.astype(dtype=int)
        df.instances_num = df.instances_num.astype(dtype=int)

        job_task_map = {}
        job_submit_time_map = {}
        for i in range(len(df)):
            series = df.iloc[i]
            job_id = series.job_id
            task_id = series.task_id

            cpu = series.cpu
            memory = series.memory
            disk = series.disk
            duration = series.duration
            submit_time = series.submit_time
            instances_num = series.instances_num

            task_configs = job_task_map.setdefault(job_id, [])
            task_configs.append(TaskConfig(task_id, instances_num, cpu, memory, disk, duration))
            job_submit_time_map[job_id] = submit_time

        job_configs = []
        for job_id, task_configs in job_task_map.items():
            job_configs.append(JobConfig(job_id, job_submit_time_map[job_id], task_configs))
        job_configs.sort(key=attrgetter('submit_time'))

        self.job_configs = job_configs

    def generate(self, offset, number):
        number = number if offset + number < len(self.job_configs) else len(self.job_configs) - offset
        ret = self.job_configs[offset: offset + number]
        the_first_job_config = ret[0]
        submit_time_base = the_first_job_config.submit_time

        tasks_number = 0
        task_instances_numbers = []
        task_instances_durations = []
        task_instances_cpu = []
        task_instances_memory = []
        for job_config in ret:
            job_config.submit_time -= submit_time_base
            tasks_number += len(job_config.task_configs)
            for task_config in job_config.task_configs:
                task_instances_numbers.append(task_config.instances_number)
                task_instances_durations.extend([task_config.duration] * int(task_config.instances_number))
                task_instances_cpu.extend([task_config.cpu] * int(task_config.instances_number))
                task_instances_memory.extend([task_config.memory] * int(task_config.instances_number))
        info=[len(ret),
              tasks_number,
              np.sum(task_instances_numbers),
              np.mean(task_instances_numbers),
              np.std(task_instances_numbers),
              np.mean(task_instances_cpu),
              np.std(task_instances_cpu),
              np.mean(task_instances_memory),
              np.std(task_instances_memory),
              np.mean(task_instances_durations),
              np.std(task_instances_durations)]
        print('Jobs number: ', info[0])
        print('Tasks number:', info[1])
        print('Tasks instances number:',info[2])

        print('Task instances number mean: ',info[3] )
        print('Task instances number std', info[4])

        print('Task instances cpu mean: ',info[5] )
        print('Task instances cpu std: ',info[6] )

        print('Task instances memory mean: ', info[7])
        print('Task instances memory std: ', info[8])

        print('Task instances duration mean: ', info[9])
        print('Task instances duration std: ',info[10])
        with open("./jobs_info.csv","w+")as f:
            line=",".join([str(i) for i in info])
            f.write(line+'\n')
        return ret
