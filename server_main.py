


print("\n\n\tStart of server------------")


import pyglet
import numpy as np
from population import Population

import Pyro4
import sys
from multiprocessing import Process
from typing import List
import time
import math

import masterclient


local_population:Population# = None # Population(50, input_size=7, hidden_size=tuple([4]), output_size=2)



@Pyro4.expose
class Job_server(object):



    def __init__(self, jobs):
        self.workers = []
        self.isDone = False
        self.job_results = []
        self.jobs = jobs

    def get_job(self):

        if len(self.jobs) > 0:
            return self.jobs.pop()
        else:
            self.isDone = True
            return None

    def get_isDone(self):
        return self.isDone

    def get_jobs_results(self):
        return self.job_results

    def get_jobs_amount(self):
        return len(self.jobs)

    def set_jobs(self, jobs):
        self.jobs = jobs

    def return_job_results(self, job_out):
        self.job_results.append(job_out)

    def register_worker(self, newworker, callback, max_jobs):
        self.workers.append((newworker, callback, max_jobs))
        print("Worker registered to labour force", newworker, callback)

    def unregister_worker(self, oldworker):
        for w, c in self.workers:
            if w == oldworker:
                self.workers.remove((w, c))
                print("Worker", oldworker, "left the labour force")
                break


class Worker:
    def __init__(self, newworker, callback, max_jobs):
        self.worker = newworker
        self.callback = callback
        self.jobs_left = max_jobs


if __name__ == "__main__":
    #server_IP = "10.19.38.66"
    server_IP = "localhost"
    print("Starting server_main.py as __main__")


    print(jobbers)

    job_server_o = Job_server(jobbers)

    main_manager = masterclient.Main_manager(server_IP)

    main_manager.start()

    JobserverDaemon = Pyro4.Daemon.serveSimple({
        job_server_o: 'Greeting',
    }, host=server_IP, port=9090, ns=False, verbose=True)


    main_manager.stop()

    print("Done with server_main.py as __main__")