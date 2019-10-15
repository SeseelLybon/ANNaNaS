

import Pyro4
import pyglet

import uuid



class Worker(object):
    def __init__(self):
        pass

def doJob(job):
    return job[0]*job[1]


expected_generation = 0

def lookforjob(dt):

    job = job_server.get_job(expected_generation, workerid)

    if job is None:
        print("Didn't get a job")

        pyglet.clock.unschedule(lookforjob)
        pyglet.clock.schedule_interval_soft(lookforjob, 2)

    else:
        print("Got a job", job)
        joboutput = doJob(job)

        job_server.return_job_results(joboutput)

        pyglet.clock.unschedule(lookforjob)
        pyglet.clock.schedule_interval_soft(lookforjob, 1)



if __name__ == '__main__':

    workerid = uuid.uuid1()

    #jobless = True
    print("Starting client; waiting for jobs")


    #ipAddressServer = "10.19.38.66" # TODO add your server remote IP here
    ipAddressServer = "localhost"


    job_server = Pyro4.core.Proxy('PYRO:Greeting@' + ipAddressServer + ':9090')
    job_server.register_worker(workerid, 50)
    pyglet.clock.schedule_interval_soft(lookforjob, 4)


    pyglet.app.run()


    print("Stopping client")