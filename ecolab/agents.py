"""
@author: Eurus.T
"""
from enum import Enum
import numpy as np



INFANT_NATURE_MOTALITY_RATE = 0.0002
ADULT_NATURE_MOTALITY_RATE = 0.0013
RHD_INFECTION_PROB = 0.6
PREGNANT_PROB = 0.4
class RHD_Status(Enum):
    """
    RHD_Status
    """
    Susceptible = 'susceptible'
    Infected = 'infected'
    Recoverd_Immune = 'immune'
    
 
class AgentType(Enum):
     """
     The type of rabbit according to different age
     """   
     Infants = 'infants'
     Adults = 'adults'
     
class Gender(Enum):
    """
    """
    Male = 1
    Female = 0
    
class Rabbit:
    """
    Base class for all types of rabbit
    """
    pregnancy_days = -1
    infected_days = -1
    maxage = 3650
    def __init__(self,position,age,rhd_status=None):
        self.position = position
        self.age = age
        self.gender = np.random.randint(0,2) ## 1 is male, 0 is female
        self.death = False
        self.rhd_status = RHD_Status.Susceptible if rhd_status == None else rhd_status
        if age < 90:
            self.speed = 0
            self.type = AgentType.Infants
        else :
            self.speed = 5
            self.type = AgentType.Adults
            # if self.gender == Gender.Female:
            #     self.reproduct_ablity = True
    
    def try_move(self, newposition, env):
        if env.check_position(newposition):
            self.position = newposition
            
    def move(self, env):
        if self.speed > 0:
            d = np.random.rand()*2*np.pi
            delta = np.round(np.array([np.cos(d),np.sin(d)]) * np.random.randint(0, self.speed + 1)) 
            self.trymove(self.position + delta, env)   
        
    def die(self):
        
        if self.rhd_status == RHD_Status.Infected and self.infected_days > 0: ##infected death begins on the 2nd infected day
            self.death = (np.random.rand() > 0.1 * self.infected_days)
        
        # nature death
        if self.age > self.maxage: self.death = True
        if self.type == AgentType.Infants:
            self.death =  (np.random.rand() < INFANT_NATURE_MOTALITY_RATE)
        else:
            self.death = (np.random.rand() < ADULT_NATURE_MOTALITY_RATE)
            
    def get_nearby_rabbit(self, position, agents):
        return [a  for a in agents if (np.abs(a.position[0] - position[0]) < 2 and np.abs(a.position[1] - position[1]) < 2)]
    
    def infection(self, agents):
        if self.type == AgentType.Adults and self.rhd_status == RHD_Status.Susceptible:
            nearby_agents = [a for a in agents if (a.rhd_status == RHD_Status.Infected and a.infected_days > 0 and np.abs(a.position[0] - self.position[0]) < 2 and np.abs(a.position[1] - self.position[1]) < 2)]
            if len(nearby_agents) > 0 and np.random.rand() <= RHD_INFECTION_PROB:
                self.infected_days = 0 ## initial day of infection
                self.rhd_status = RHD_Status.Infected

    def reproduct(self, agents):
        if self.type == AgentType.Adults and self.gender == Gender.Female and self.pregnancy_days == -1:
            same_grid_male = [a for a in agents if (a.type == AgentType.Adults and a.gender == Gender.Male and a.position == self.position)]
            prob = np.random.randint(11,83) / 100
            if len(same_grid_male) > 0 and np.random.rand() <= prob:
                self.pregnancy_days = 0
                
    def born_new_rabbit(self):
        if self.pregnancy_days > 30:
            litter_num = np.random.randint(2, 8)
            newborn =[]
            i = 0
            for i in range(litter_num):
                newborn +=  Rabbit(position = self.position, age = 1)
                i += 1
            self.pregnancy_days = -1
            return newborn
        
        return None
            
    
    def other_daily_grow(self, agents): # run this function first in each day loop
        self.age +=1
        if self.pregnancy_days > -1:
            self.pregnancy_days += 1
        
        if self.rhd_status == RHD_Status.Infected:
            self.infected_days += 1
        
        if self.infected_days > 10:
            self.rhd_status == RHD_Status.Recoverd_Immune
            self.infected_days = -1
            
            
        if self.age > 90:
            self.speed = 5
            self.type = AgentType.Adults
            
            
    def summary_vector(self):
        return [self.position[0], self.position[1], self.type, self.rhd_status]