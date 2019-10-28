

import Pyro4
import pyglet
import time

import uuid

import client_core
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


    ipAddressServer = sys.argv[1]
    work_slots = int(sys.argv[2])


    job_server = Pyro4.core.Proxy('PYRO:Greeting@' + ipAddressServer + ':9090')
    job_server.register_worker(workerid, work_slots)
    print(job_server.get_workers_amount())
    pyglet.clock.schedule_interval_soft(lookforjob, 4)


    pyglet.app.run()


    print("Stopping client")