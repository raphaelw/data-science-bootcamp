import random
import json

import numpy as np

"""
User Story:
    - As a data scientist
    - I want to be able to customize the customer behaviour,
    - so that I can animate different customer models.
"""

class CustomerModelDummy:
    def __init__(self, customer_id=1):
        self.state = 'entrance'

    def get_state(self): # -> (state, duration)
        return self.state, 1.5

    def next_state(self):
        if self.state == 'entrance':
            self.state = 'fruit'
        elif self.state == 'fruit':
            self.state = 'dairy'
        elif self.state == 'dairy':
            self.state = 'checkout'
        else:
            self.state = None

    def done(self): # -> bool
        return self.state is None

class CustomerModel:
    """Cutomer model based on MCMC."""
    def __init__(self, customer_id=1):
        with open('data/transition_matrix.json', 'rb') as f:
            self._transition_matrix = json.load(f)
        with open('data/mean_durations.json', 'rb') as f:
            self._mean_durations = json.load(f)

        self.state = 'entrance'
        self.duration = 0.5 * customer_id
        self.duration = 1.5 # black friday

    def get_state(self):
        """Returns tuple containing: state, duration"""
        return self.state, self.duration

    def next_state(self):
        """Transition to next state.
        Returns tuple containing: state, duration"""
        if self.state == 'checkout':
            self.state = None
            self.duration = 0.
        
        if self.state is None:
            return
        
        # Monte Carlo
        last_state = self.state
        probability_mass_function = self._transition_matrix[last_state]
        self.state = random.choices(population=list(probability_mass_function.keys())
                                    , weights=probability_mass_function.values()
                                    , k=1)[0]
        
        if self.state == 'checkout':
            self.duration = 3.
        else:
            # exponential distribution sampling for time spent in a section
            mean = self._mean_durations[self.state]
            lambd = 1/mean
            self.duration = random.expovariate(lambd=lambd)

    def done(self):
        return self.state is None


class CustomerModelRandom:
    """Cutomer dummy model. Completely random transitions."""
    def __init__(self, customer_id=1):
        self.state = 'entrance'
        self.duration = random.random()*5
        self.duration = customer_id*0.5
        self.duration = 1.

    def get_state(self):
        """Returns tuple containing: state, duration"""
        return self.state, self.duration

    def next_state(self):
        """Transition to next state.
        Returns tuple containing: state, duration"""
        if self.state == 'checkout':
            self.state = None
            self.duration = 0.
        
        if self.state is None:
            return
        
        while True:
            choice = random.choice(['drinks', 'fruit', 'spices', 'dairy', 'checkout'])
            if not choice == self.state:
                self.state = choice
                self.duration = random.random()*5
                return self.get_state()
    
    def done(self):
        return self.state is None


if __name__ == '__main__':
    c = CustomerModel(22)
    print(c._transition_matrix['checkout'])
    print('')
    print(c._durations)
