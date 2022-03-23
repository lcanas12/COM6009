import numpy as np
import matplotlib
from ecolab.agents import Rabbit, RHD_Status
import matplotlib.pyplot as plt

def run_ecolab(env, agents, Niteration=360, earlystop=True):

    record=[] #TODO
    for it in range(Niteration):
        month = (it / 30) % 12  ## 0~11 ->  Jan~Dec
        for agent in agents:
            agent.other_daily_grow(agents)
            if month > 3:
                agent.reproduct(agents)
            agent.move()
            agent.die()
            
        agents = [a for a in agents if a.death == False]
        for agent in agents:
            agent.infection(agents)
            newborn = agent.born_new_rabbit()
            if newborn is not None:
                agent += newborn
        
        
        record.append({'susceptible agents': np.array([a.summary_vector() for a in agents a.rhd_status == RHD_Status.Infected]),
                      {'infected agents': np.array(a.summary_vector() for a in agents)} )        
        
                
            
            