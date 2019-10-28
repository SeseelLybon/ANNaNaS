




import Pyro4


from multiprocessing import Process
import time
from typing import List
from population import Population
import serpent
import os

from enum import Enum
from enum import auto

class States(Enum):
    initializing = auto()
    has_jobs_ready = auto()
    waiting_for_clients_results = auto()
    processing_results = auto()
    done = auto()

master_population = Population(400, input_size=7, hidden_size=tuple([0]), output_size=2)

class Main_manager:

    def __init__(self, IP): # , input_size, hidden_size, output_size):
        self.state = States.initializing
        self.local_job_server = Pyro4.core.Proxy('PYRO:Greeting@' + IP + ':9090')
        #self.local_population:Population = master_population
        self.job_results = []
        self.main_process = Process(target=self.run)

        #create if not there, or overwrite with nothing if there
        with open("spreadsheetdata.txt", "w+") as f:
            f.write("")


    def start(self):
        print("client: Starting master client")
        self.main_process.start()

    def stop(self):
        print("client: Stopping master client")
        self.main_process.close()

    def run(self):
        print("client: Started main() as process")


        self.local_job_server.set_jobs(master_population.pickle_population_to_list())

        self.waiting_for_isDone()


        print("client: Returning from main()")


    def waiting_for_isDone(self):

        while self.state is not States.done:

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