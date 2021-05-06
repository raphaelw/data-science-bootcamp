import random

class CustomerModel:
    """Cutomer dummy model. Completely random transitions."""
    def __init__(self, customer_id=1):
        self.state = 'entrance'
        self.duration = random.random()*5

    def get_state(self):
        """Returns tuple containing: state, duration"""
        return self.state, self.duration

    def next_state(self):
        """ Transition to next state.
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
