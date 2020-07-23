



import Pyro4
import masterclient
import sys
from population import Population
import time



class Worker:
    def __init__(self, workerID, work_slots):
        self.workerID = workerID
        self.work_slots = work_slots
        self.isWorkingOnJobs = False
        self.claimedMeeps = [] # backup of all the meeps the worker claimed in case he died.
        self.isAlive = True
        self.lastTimeStamp = 0

@Pyro4.expose
class Job_server(object):

    def __init__(self, pop_size, inputsize, hiddensize, outputsize):
        self.workers:dict = {}
        self.hasUnworkedMeeps = False
        self.hasAllResults = False
        self.unworked_meeps = []
        self.results = []
        self.current_generation = 0
        self.max_jobs:int = pop_size    # Size of population of master_client

        self.inputsize = inputsize
        self.hiddensize = hiddensize
        self.outputsize = outputsize


    def get_job(self, workerid):
        if self.workers.get(workerid, None) is None:
            return "Not registered"

        if len(self.unworked_meeps) == 0:
            return None

        claimed_meeps = self.unworked_meeps[:self.workers[workerid].work_slots]
        self.workers[workerid].claimedMeeps += self.unworked_meeps[:self.workers[workerid].work_slots]
        self.unworked_meeps[:] = self.unworked_meeps[self.workers[workerid].work_slots:]
        return claimed_meeps


    def return_results(self, workerid, x):
        self.results += x
        self.workers[workerid].isWorkingOnJobs = False
        self.workers[workerid].claimedMeeps.clear()


    def get_hasUnworkedMeeps(self)->bool:
        if len(self.unworked_meeps) > 0:
            return True
        else:
            return False


    def test_hasAllResults(self)->bool:
        # If there are no meeps to be processed
        # and none of the workers mention they have claimed meeps
        # and the amount of results equals the max amount of jobs Masterclient has given.
        # then I'll assume that all meeps have been processed.
        if  len(self.workers) > 0 and\
                len([True for worker in self.workers.values() if worker.isWorkingOnJobs]) == 0 and\
                len(self.unworked_meeps) == 0 and\
                len(self.results) == self.max_jobs:
            return True
        else:
            return False


    def get_hasAllResults(self):
        return self.hasAllResults

    def get_jobs_results(self):
        return self.results

    def get_jobs_amount(self):
        return len(self.unworked_meeps)

    def get_claimed_jobs_amount(self):
        return sum([self.workers[wid] for wid in self.workers])

    def get_results_amount(self):
        return len(self.results)

    def get_workers_amount(self):
        return len(self.workers)

    def get_workers(self):
        return [ x.workerID for x in self.workers.values() ]


    def get_registered_slots(self):
        return sum( [ x.work_slots for x in self.workers.values() ] )


    def set_jobs(self, jobs):
        self.unworked_meeps = jobs
        self.results.clear()


    def set_current_generation(self, cur_gen:int):
        self.current_generation = cur_gen


    def return_job_results(self, workerid, worked_meeps):
        self.worked_meeps.append(worked_meeps)
        self.workers[workerid].hasReturnedResults = True


    def register_worker(self, workerid, work_slots):
        self.workers[workerid] = Worker(workerid, work_slots)
        print("Jobserver:", self.get_registered_slots())
        #print("Jobserver:", self.workers.keys())
        print("Jobserver:", "Worker registered to labour force", workerid)
        return self.inputsize, self.hiddensize, self.outputsize


    def register_alive(self, workerid):
        #print("Debug; ", workerid)
        #print("Debug;", self.workers.keys())
        self.workers[workerid].isAlive = True


    def test_ifWorkersAlive(self)->bool:
        deadworkers = []

        # TODO: UTTERLY FUCKING BREAKS SOMEHOW!?

        for worker in self.workers.values():
            if not worker.isAlive:
                # Worker hasn't marked itself as alive since the last time this was ran
                deadworkers.append(worker.workerID)
                #if self.workers[worker.workerID].isWorkingOnJobs:
                self.unworked_meeps += self.workers[worker.workerID].claimedMeeps
                self.hasUnworkedMeeps = True
                continue
            else:
                #Set them all to false as they have to set it to true again.
                worker.isAlive = False

        if len(deadworkers) > 0:
            for deadworkerid in deadworkers:
                self.workers.pop(deadworkerid)
                print("Jobserver:", "Worker", deadworkerid, "left the building")
            return False
        else:
            return True




if __name__ == "__main__":

    max_attempts = 10  # amount of attempts a mastermind can make before being considered dead
    max_dif_pegs = 5  # numbers simulate the diffirent colours of pegs
    max_pegs = 4  # how many pegs have to be guessed

    server_IP = sys.argv[1]
    pop_size = int(sys.argv[2])
    if len(sys.argv) == 4:
        load_from_save = sys.argv[3]
    else:
        load_from_save =  "False"

    inputsize=max_pegs*max_attempts*2
    hiddensize=tuple([max_pegs*max_attempts, max_pegs*max_dif_pegs])
    outputsize=max_dif_pegs*max_pegs

    print("Server: Starting server_main.py as __main__")
    #server_IP = "10.19.38.66"
    #server_IP = "localhost"

    main_manager = masterclient.Main_manager(server_IP, pop_size, inputsize, hiddensize, outputsize, load_from_save)

    main_manager.start()

    job_server_o = Job_server(pop_size, inputsize, hiddensize, outputsize)

    JobserverDaemon = Pyro4.Daemon.serveSimple({
        job_server_o: 'Greeting',
    }, host=server_IP, port=9090, ns=False, verbose=True)


    main_manager.stop()

    print("Server: Done with server_main.py as __main__")