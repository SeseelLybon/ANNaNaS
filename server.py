


print("\n\n\tStart of server------------")


import pyglet
import numpy as np
from population import Population



checkclient_isDone_interval = 10 # seconds

local_population:Population# = None # Population(50, input_size=7, hidden_size=tuple([4]), output_size=2)

def gather_sort_create_send():
    # ask all clients for their meeps
    # call NaturalSelection() of the server population
    # send meeps to the clients based on how many a client registered for

    pyglet.clock.schedule_interval_soft(check_if_clients_are_done, checkclient_isDone_interval)
    pass

def gather_meeps_from_clients():
    # for clnt in clients:
    #   clnt.get_meeps()
    pass

def check_if_clients_are_done(dt):
    pass
    # for clnt in clients:
    #   if is_client_Done(clnt):
    #       return # Not done
    # pyglet.clock.unschedule(check_if_clients_are_done) #unschedule self
    # gather_sort_create_send()


def is_client_Done(client):
    # ping client if he's done
    pass


class Client:
    def __init__(self, id, IP, size):
        self.id=id
        self.IP = IP
        self.size = size




pyglet.app.run()



print("\n\n\tEnd of server------------")