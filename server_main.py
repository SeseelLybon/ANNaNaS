



import Pyro4


import masterclient



class Worker:
    def __init__(self, workerID, work_slots):
        self.workerID = workerID
        self.work_slots = work_slots
        self.hasClaimedSlots = False
        self.hasReturnedResults = False

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
            if len(self.unworked_meeps) == 0:
                self.hasUnworkedMeeps = True
            return self.unworked_meeps[:self.workers[workerid].work_slots]
        else:
            return False

    def return_results(self, x):
        self.results.append(x)

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

    def set_current_generation(self, cur_gen:int):
        self.current_generation = cur_gen

    def return_job_results(self, workerid, worked_meeps):
        self.worked_meeps.append(worked_meeps)
        self.workers[workerid].hasReturnedResults = True

    def register_worker(self, workerid, work_slots):
        self.workers[workerid] = Worker(workerid, work_slots)
        #self.max_slots += work_slots
        print("Jobserver:", self.get_registered_slots())
        print("Jobserver:", self.workers.keys())
        print("Jobserver:", "Worker registered to labour force", workerid)

#    def unregister_worker(self, workerid):
#        self.max_slots-= self.workers[workerid]
#        self.workers.pop(workerid)
#        print("Jobserver:", "Worker", workerid, "left the labour force")




if __name__ == "__main__":

    print("Server: Starting server_main.py as __main__")
    #server_IP = "10.19.38.66"
    server_IP = "localhost"

    main_manager = masterclient.Main_manager(server_IP)

    main_manager.start()

    job_server_o = Job_server()

    JobserverDaemon = Pyro4.Daemon.serveSimple({
        job_server_o: 'Greeting',
    }, host=server_IP, port=9090, ns=False, verbose=True)


    main_manager.stop()

    print("Server: Done with server_main.py as __main__")