import logging
from apscheduler.scheduler import Scheduler


class Job_Manager(object):

    def __init__(self, config):
        self.scheduler = Scheduler(config["SCHEDULER"])
        if self.scheduler is not None:
            self.scheduler.start()

    def add_job(self, task, interval, name, *args):
        args = args if args is not None else None
        self.scheduler.add_interval_job(task, seconds=interval, args=args,  name=name, max_instances=50)

    def remove_job(self, name):
        matchedJobs = self.__get_jobs(name)
        self.__remove_jobs(matchedJobs)

    def __get_jobs(self, name):
        return [job for job in self.scheduler.get_jobs() if job.name == name]

    def __remove_jobs(self, matchedJobs):
        for job in matchedJobs:
            self.scheduler.unschedule_job(job)




