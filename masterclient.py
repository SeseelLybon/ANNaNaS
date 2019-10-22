




import Pyro4


from multiprocessing import Process
import time
from typing import List
from population import Population
import serpent

from enum import Enum
from enum import auto

class States(Enum):
    initializing = auto()
    has_jobs_ready = auto()
    waiting_for_clients_results = auto()
    processing_results = auto()
    done = auto()

master_population = Population(100, input_size=7, hidden_size=tuple([4]), output_size=2)

class Main_manager:

    def __init__(self, IP): # , input_size, hidden_size, output_size):
        self.state = States.initializing
        self.local_job_server = Pyro4.core.Proxy('PYRO:Greeting@' + IP + ':9090')
        #self.local_population:Population = master_population
        self.job_results = []
        self.main_process = Process(target=self.run)


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
                print("All meeps have been tested and returned")

                # Future note; we do actually need the brains from the clients because we might run Backpropegation on them.
                # In that case, the brain *does* change and is important to us!
                ser_bytes = self.local_job_server.get_jobs_results()
                master_population.unpickle_population_from_list(ser_bytes)

                #TODO run natural selection
                master_population.naturalSelection()

                #TODO send population back to server
                self.state = States.has_jobs_ready
            else:
                print("Not all jobs are done...")
                print(self.local_job_server.get_jobs_amount())
                time.sleep(10)