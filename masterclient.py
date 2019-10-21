




import Pyro4


from multiprocessing import Process
import time
from typing import List
from population import Population

from enum import Enum
from enum import auto

class States(Enum):
    has_jobs_ready = auto()
    waiting_for_clients_results = auto()
    processing_results = auto()
    done = auto()







class Main_manager:

    def __init__(self, IP, popsize): # , input_size, hidden_size, output_size):
        self.state = States.waiting_for_client_connections
        self.local_job_server = Pyro4.core.Proxy('PYRO:Greeting@' + IP + ':9090')
        self.local_population:Population = Population(popsize, input_size=7, hidden_size=tuple([4]), output_size=2)
        self.job_results = []
        self.main_process = Process(target=self.run)


    def start(self):
        print("client: Starting master client")
        self.main_process.start()

    def stop(self):
        print("client: Stopping master client")
        self.main_process.close()

    def run(self):
        global local_population
        print("client: Started main() as process")

        local_population = Population(5, input_size=7, hidden_size=tuple([4]), output_size=2)

        self.waiting_for_isDone()


        print("client: Returning from main()")


    def waiting_for_isDone(self):

        while self.state is not States.done:

            # TODO: Overhaul; rather than making jobs equal to what workers provide, set up fixed jobs and let workes
            #   pop how many they want to work on. This is easier than overhauling Population to deal with variable
            #   amounts of population sizes.
            # TODO: That said, if a worker dies while working, the meeps he claimed are all lost.
            print("client: --------")



            if self.state is States.waiting_for_client_connections:
                print("Registered workers:", self.local_job_server.get_workers_amount() )
                if self.local_job_server.get_workers_amount() == 0:
                    print( self.local_job_server.get_jobs_results() )
                    print("Clients have yet to connect.")
                    print("Can't work without clients in the labour force")
                    time.sleep(5)
                else:
                    print("No code 1")
                    # TODO: switch states and distrebute jobs
            else:
                print("Testing if clients are done")
                if self.local_job_server.test_hasAllResults():
                    print("All meeps have been tested and returned")
                    self.job_results = self.local_job_server.get_jobs_results()
                    print(self.job_results)
                    #TODO run natural selection
                else:
                    print("Not all jobs are done...")
                    print(self.local_job_server.get_jobs_amount())
                    time.sleep(5)