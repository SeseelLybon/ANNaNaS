


print("\n\n\tStart of server------------")


import pyglet
import numpy as np
from population import Population

import Pyro4
from multiprocessing import Process
from typing import List
import time
import math
import uuid

import masterclient

local_population:Population# = None # Population(50, input_size=7, hidden_size=tuple([4]), output_size=2)



@Pyro4.expose
class Job_server(object):

    def __init__(self):
        self.workers:dict = {}
        self.hasUnworkedMeeps = False
        self.hasAllResults = False
        self.unworked_meeps = []
        self.results = []
        self.max_slots = 0
        self.current_generation = 0

    def get_job(self, workerid):
        if not self.workers[workerid].hasClaimedSlots:
            self.workers[workerid].hasClaimedSlots = True
            #TODO: check if all the meeps have been claimed, then set self.hasUnworkedMeeps = True
            return self.unworked_meeps[:self.workers[workerid].work_slots]
        else:
            return False

    def get_hasUnworkedMeeps(self)->bool:
        if len(self.unworked_meeps) > 0:
            self.hasUnworkedMeeps = True
            return True
        else:
            self.hasUnworkedMeeps = False
            return False

    def test_hasAllResults(self)->bool:
        if len(self.results) == self.max_slots:
            self.hasAllResults = True
            return True
        else:
            self.hasAllResults = False
            return False

    def get_hasAllResults(self):
        return self.hasAllResults

    def get_jobs_results(self):
        return self.worked_meeps

    def get_jobs_amount(self):
        return len(self.unworked_meeps)

    def set_jobs(self, jobs):
        self.unworked_meeps = jobs

    def set_current_generation(self, cur_gen:int):
        self.current_generation = cur_gen

    def return_job_results(self, workerid, worked_meeps):
        self.worked_meeps.append(worked_meeps)
        self.workers[workerid].hasReturnedResults = True

    def register_worker(self, workerid, work_slots):
        self.workers[workerid] = Worker(workerid, work_slots)
        self.max_slots += work_slots
        print("Worker registered to labour force", workerid, self.workers[workerid])

    def unregister_worker(self, workerid):
        self.max_slots-= self.workers[workerid]
        self.workers.pop(workerid)
        print("Worker", workerid, "left the labour force")


class Worker():
    def __init__(self, workerID, work_slots):
        self.workerID = workerID
        self.work_slots = work_slots
        self.hasClaimedSlots = False
        self.hasReturnedResults = False


if __name__ == "__main__":
    print("Starting server_main.py as __main__")
    #server_IP = "10.19.38.66"
    server_IP = "localhost"

    main_manager = masterclient.Main_manager(server_IP)

    main_manager.start()

    JobserverDaemon = Pyro4.Daemon.serveSimple({
        Job_server: 'Greeting',
    }, host=server_IP, port=9090, ns=False, verbose=True)


    main_manager.stop()

    print("Done with server_main.py as __main__")