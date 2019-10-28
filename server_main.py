



import Pyro4
import masterclient
import sys
from population import Population



class Worker:
    def __init__(self, workerID, work_slots):
        self.workerID = workerID
        self.work_slots = work_slots
        self.isWorkingOnJobs = False
        self.claimedMeeps = [] # backup of all the meeps the worker claimed in case he died.
        self.isAlive = True

@Pyro4.expose
class Job_server(object):

    def __init__(self, pop_size):
        self.workers:dict = {}
        self.hasUnworkedMeeps = False
        self.hasAllResults = False
        self.unworked_meeps = []
        self.results = []
        self.current_generation = 0
        self.max_jobs:int = pop_size    # Size of population of master_client

    def get_job(self, workerid):
        if len(self.unworked_meeps) == 0:
            self.workers[workerid].isWorkingOnJobs = True
            self.hasUnworkedMeeps = True
        claimed_meeps = self.unworked_meeps[0:self.workers[workerid].work_slots]
        self.unworked_meeps[:] = self.unworked_meeps[self.workers[workerid].work_slots:]
        return claimed_meeps

    def return_results(self, workerid, x):
        self.results += x
        self.workers[workerid].isWorkingOnJobs = False

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
        # TODO: probably overkill. Unless there's a glitch, results should never exceed max_results
        #   Though if a worker dies before it returns the results, the program locks up.
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
        self.results = [] # TODO: probably shouldn't do this here

    def set_current_generation(self, cur_gen:int):
        self.current_generation = cur_gen

    def return_job_results(self, workerid, worked_meeps):
        self.worked_meeps.append(worked_meeps)
        self.workers[workerid].hasReturnedResults = True

    def register_worker(self, workerid, work_slots):
        self.workers[workerid] = Worker(workerid, work_slots)
        print("Jobserver:", self.get_registered_slots())
        print("Jobserver:", self.workers.keys())
        print("Jobserver:", "Worker registered to labour force", workerid)

    # TODO: implement unregister_worker for catching clients that die or loose connection
#    def unregister_worker(self, workerid):
#        self.workers.pop(workerid)
#        print("Jobserver:", "Worker", workerid, "left the labour force")




if __name__ == "__main__":

    server_IP = sys.argv[1]
    pop_size = int(sys.argv[2])

    print("Server: Starting server_main.py as __main__")
    #server_IP = "10.19.38.66"
    #server_IP = "localhost"

    main_manager = masterclient.Main_manager(server_IP, pop_size)

    main_manager.start()

    job_server_o = Job_server(pop_size)

    JobserverDaemon = Pyro4.Daemon.serveSimple({
        job_server_o: 'Greeting',
    }, host=server_IP, port=9090, ns=False, verbose=True)


    main_manager.stop()

    print("Server: Done with server_main.py as __main__")