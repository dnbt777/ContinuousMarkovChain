import random
import numpy as np
from scipy.special import softmax


chain = {
    0 : [((1, 100), (2, 3))]
   #state : [[next_state, count]]
}

class ContinuousMarkovChain():
    def __init__(self, sequences, attractor_coefficient=2):       
        self.chain_states = {} # init the chain
        self.sequences = sequences # store seqs in case I need em later
        for seq in sequences:
            hashable_seq = to_hashable(seq)
            self.populate_chain_states(hashable_seq) # update chain w sequences
        self.attractor_coefficient = attractor_coefficient # 2 for gravity, 1 for linear, etc
        self.temperature = 1 # does nothing for now - make this scale probabilities
    
    
    def populate_chain_states(self, seq):
        for i, element in enumerate(seq):
            if i == len(seq) - 1: # last index ends it
                future_state = None
            else:
                future_state = seq[i+1]
            
            self.update_chain_state(element, future_state)
        print("Updated chain state with sequence")
            
    
    def update_chain_state(self, element, future_state):
        element = to_hashable(element)
        if element in self.chain_states:
            self.chain_states[element].append(future_state)
        else:
            self.chain_states.update({element : [future_state]})
    
    
    def get_next_state(self, current_state):
        # current state does NOT NEED TO BE IN SEQ AT ALL!!!!!!!!!!!!!!!!!!!!!!!!!!!! WTHAT?!?!?!?!
        elements, next_states = list(self.chain_states.keys()), list(self.chain_states.values())
        
        distances = np.array([distance(current_state, elem) for elem in elements]) # precompute this
        #print(distances[:5])
        epsilon = 0.00000001 # prevents errors
        gravities = np.array([1/(epsilon + r**self.attractor_coefficient) for r in distances])
        gravities = gravities / self.temperature
        probabilities = softmax(gravities)
        

        #sorted_next_states = list(zip(*sorted(zip(gravities, next_states), key=lambda pair: pair[0])))[0]
        #print(sorted_next_states[:5])

        next_state = random.choices(next_states, weights=probabilities, k=1)
        #print(next_states[:100])

        if len(next_state) > 1:
            next_state = random.choice(next_state)
        
        return next_state[0][0]


def distance(a, b):
    if not len(a) == len(b): # same dimension for both
        print(a, b)
        raise Exception("A and B must have same dimension")
    dim = len(a)
    if dim == 1:
        return np.abs(a-b)
    else:
        return np.sqrt(np.sum([(an - bn)**2 for an, bn in zip(a, b)]))


def to_hashable(obj):
    if isinstance(obj, np.ndarray):
        # If the array is of a basic type (e.g., integers, floats), convert directly
        return tuple(obj)
    return obj