




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

    def __init__(self, IP, pop_size, inputsize, hiddensize, outputsize, load_from_file):
        global master_population

        self.state = States.initializing

        self.local_job_server = Pyro4.core.Proxy('PYRO:Greeting@' + IP + ':9090')
        self.job_results = []
        self.main_process = Process(target=self.run, args=(pop_size, inputsize, hiddensize, outputsize, load_from_file,))

        if load_from_file == "False":
            #create if not there, or overwrite with nothing if there
            with open("spreadsheetdata.txt", "w+") as f:
                f.write("")
        else:
            pass
            # Continue appending to the existing file that should still be valids


    def start(self):
        print("client: Starting master client")

        self.main_process.start()

    def stop(self):
        print("client: Stopping master client")
        self.main_process.close()

    def run(self, pop_size, inputsize, hiddensize, outputsize, load_from_file):
        global master_population
        print("client: Started main() as process")
        print(load_from_file)
        if load_from_file == "True":
            try:
                master_population = Population(pop_size, input_size=inputsize, hidden_size=hiddensize, output_size=outputsize, isHallow=True)
                master_population.unpickle_population_from_file()
            except FileNotFoundError:
                master_population = Population(pop_size, input_size=inputsize, hidden_size=hiddensize, output_size=outputsize)

        else:
            master_population = Population(pop_size, input_size=inputsize, hidden_size=hiddensize, output_size=outputsize)


        self.local_job_server.set_jobs(master_population.pickle_population_to_list())

        self.waiting_for_isDone()


        print("client: Returning from main()")



    def waiting_for_isDone(self):

        # The issue of workers getting kicked out by the server because they don't reply in time is a blocking function
        #   issue on the worker side.
        # Unsure how to fix though, since "population.updateAlive()" can take an arbetrary long amount of time to run.
        # Any speed up gained in this function is only temporary to whenever I use a bigger ANN + update() function.
        # Best solution is to somehow offload the 'ping server I'm alive' function. Like a second progres;
        #   but this one wouldn't crash if the client crashes.
        # That said, this function doesn't actually have to ping a large amount of times anyway, so in that regard I can
        #   could justify delaying the inevitable. But this is gonna bound up showing up eventually.

        lasttime = 0
        while self.state is not States.done:

            curtime = time.time()
            if curtime-lasttime >= 120:
                print("Testing if all workers were alive - ", end="")
                print("all workers alive? ", self.local_job_server.test_ifWorkersAlive() )
                lasttime = curtime
            else:
                #print("skipped testing if workers are alive")
                pass

            #print("client: --------")


            #print("Testing if clients are done:", end="")
            if self.local_job_server.test_hasAllResults():
                self.state = States.processing_results
                print("\nAll meeps have been tested and returned to the warehouse")

                # Future note; we do actually need the brains from the clients because we might run Backpropegation on them.
                # In that case, the brain *does* change and is important to us!
                ser_bytes = self.local_job_server.get_jobs_results()
                master_population.unpickle_population_from_list(ser_bytes)

                #run natural selection
                print("Starting natural selection")
                master_population.naturalSelection()

                print("Pickling best meep of this generation, with his score of", master_population.bestMeeple.brain.score)
                print("... I hope that's a high score.")
                master_population.pickle_bestmeep_to_file()

                print("Done Natural Selection/MachineLearning. Sending", len(master_population.pop),"jobs to warehouse")
                # send population back to server
                self.local_job_server.set_jobs(master_population.pickle_population_to_list())
                master_population.pickle_population_to_file()
                self.state = States.has_jobs_ready
                print("Starting generation", master_population.generation)
            else:
                #print("Not all jobs are done...")
                #print(self.local_job_server.get_jobs_amount(),
                #      self.local_job_server.get_claimed_jobs_amount(),
                #      self.local_job_server.get_results_amount())
                time.sleep(10)