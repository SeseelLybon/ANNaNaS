




import Pyro4


from multiprocessing import Process
import time
from population import Population
import time

from enum import Enum
from enum import auto

class States(Enum):
    initializing = auto()
    has_jobs_ready = auto()
    waiting_for_clients_results = auto()
    processing_results = auto()
    done = auto()

master_population:Population# = Population(200, input_size=7, hidden_size=tuple([0]), output_size=2)

class Main_manager:

    def __init__(self, IP, pop_size): # , input_size, hidden_size, output_size):
        global master_population

        self.state = States.initializing

        self.local_job_server = Pyro4.core.Proxy('PYRO:Greeting@' + IP + ':9090')
        self.job_results = []
        self.main_process = Process(target=self.run, args=(pop_size,))

        #create if not there, or overwrite with nothing if there
        with open("spreadsheetdata.txt", "w+") as f:
            f.write("")


    def start(self):
        print("client: Starting master client")

        self.main_process.start()

    def stop(self):
        print("client: Stopping master client")
        self.main_process.close()

    def run(self, pop_size):
        global master_population
        print("client: Started main() as process")

        master_population = Population(pop_size, input_size=7, hidden_size=tuple([0]), output_size=2)

        self.local_job_server.set_jobs(master_population.pickle_population_to_list())

        self.waiting_for_isDone()


        print("client: Returning from main()")



    def waiting_for_isDone(self):


        lasttime = 0
        while self.state is not States.done:

            curtime = time.time()
            if curtime-lasttime >= 30:
                print("Testing if all workers were alive")
                print("all workers alive?", self.local_job_server.test_ifWorkersAlive())
                lasttime = curtime
            else:
                #print("skipped testing if workers are alive")
                pass

            print("client: --------")


            print("Testing if clients are done")
            if self.local_job_server.test_hasAllResults():
                self.state = States.processing_results
                print("All meeps have been tested and returned to the warehouse")

                # Future note; we do actually need the brains from the clients because we might run Backpropegation on them.
                # In that case, the brain *does* change and is important to us!
                ser_bytes = self.local_job_server.get_jobs_results()
                master_population.unpickle_population_from_list(ser_bytes)

                #TODO run natural selection
                print("Starting natural selection")
                master_population.naturalSelection()

                print("Done Natural Selection/MachineLearning. Sending jobs to warehouse")
                #TODO send population back to server
                self.local_job_server.set_jobs(master_population.pickle_population_to_list())
                self.state = States.has_jobs_ready
                print("Starting generation", master_population.generation)
            else:
                print("Not all jobs are done...")
                print(self.local_job_server.get_jobs_amount(), self.local_job_server.get_results_amount())
                time.sleep(10)