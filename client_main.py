

import Pyro4
import pyglet
import time

import uuid

import client_core
from population import Population
import sys

def test_isDone(dt):
    if client_core.client_isDone:
        print("Returning dino brains")
        pyglet.clock.unschedule(test_isDone)
        return_results()


def return_results():
    global job_server
    global workerid

    job_server.return_results(workerid, client_core.client_population.pickle_population_to_list())
    pyglet.clock.schedule_interval_soft(lookforjob, lookforjob_TIMEOUT)
    print("Looking for jobs again")


def register_alive(dt):
    global job_server
    print("Telling server I am still alive")
    job_server.register_alive(workerid)


def lookforjob(dt):
    global job_server
    print("--------")

    if job_server.get_hasUnworkedMeeps() == 0:
        print("No jobs queued")

        pyglet.clock.unschedule(lookforjob)
        pyglet.clock.schedule_interval_soft(lookforjob, lookforjob_TIMEOUT)
        return

    jobs = job_server.get_job(workerid)

    if jobs is None:
        print("Didn't get a job")

        pyglet.clock.unschedule(lookforjob)
        pyglet.clock.schedule_interval_soft(lookforjob, lookforjob_TIMEOUT)
        return
    elif jobs == "Not registered":
        pyglet.app.exit()
        print("Worker was not registered to the server for some reason, but is still alive.")
        print("This shouldn't have happened.")
        return

    else:
        print("Got a job")
        pyglet.clock.unschedule(lookforjob)
        pyglet.clock.schedule_interval_soft(test_isDone, 10)

        client_core.dojob(job=jobs)

workerid = None

lookforjob_TIMEOUT = 10 # seconds

if __name__ == '__main__':

    workerid = uuid.uuid1()

    #jobless = True
    print("Starting client; waiting for jobs")

    try:
        ipAddressServer = sys.argv[1]
        work_slots = int(sys.argv[2])
    except IndexError:
        ipAddressServer = "localhost"
        work_slots = 50

    job_server = Pyro4.core.Proxy('PYRO:Greeting@' + ipAddressServer + ':9090')
    client_core.inputsize, client_core.hiddensize, client_core.outputsize = job_server.register_worker(workerid, work_slots)
    pyglet.clock.schedule_interval_soft(lookforjob, 4)
    pyglet.clock.schedule_interval_soft(register_alive, 15)

    try:
        pyglet.app.run()
    except Pyro4.errors.ConnectionClosedError:
        pass


    print("Stopping client")