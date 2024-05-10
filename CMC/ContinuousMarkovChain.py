import random
import numpy as np
from scipy.special import softmax

class ContinuousMarkovChain():
    def __init__(self, sequences, attractor_coefficient=2):
        self.chain_states = {}  # Initialize the chain
        self.sequences = sequences  # Store sequences for potential future use
        
        for seq in sequences:
            hashable_seq = to_hashable(seq)
            print(len(hashable_seq))
            self.populate_chain_states(hashable_seq)  # Update chain with sequences
        self.attractor_coefficient = attractor_coefficient  # Coefficient for gravity effect
        self.temperature = 1  # Placeholder for potential temperature scaling
    
    def populate_chain_states(self, seq):
        for i, element in enumerate(seq):
            if i == len(seq) - 1:  # Last index ends it
                future_state = None
            else:
                future_state = seq[i+1]
            
            self.update_chain_state(element, future_state)
        print("Updated chain state with sequence")
    
    def update_chain_state(self, element, future_state):
        element, future_state = to_hashable(element), to_hashable(future_state)
        if element in self.chain_states:
            if future_state in self.chain_states[element]:
                self.chain_states[element][future_state] += 1
            else:
                self.chain_states[element][future_state] = 1
        else:
            self.chain_states[element] = {future_state : 1}
    
    def get_next_state(self, current_state):
        elements, state_dicts = list(self.chain_states.keys()), list(self.chain_states.values())
        
        distances = np.array([distance(current_state, elem) for elem in elements])
        epsilon = 0.00000001  # Prevents division by zero
        gravities = np.array([1 / (epsilon + r**self.attractor_coefficient) for r in distances])
        gravities = gravities / self.temperature
        probabilities = softmax(gravities)
        
        chosen_element = random.choices(elements, weights=probabilities, k=1)[0]
        next_states = self.chain_states[chosen_element]
        
        # Weight next states by their counts
        next_state_keys = list(next_states.keys())
        next_state_values = list(next_states.values())
        next_state_probabilities = softmax(next_state_values)
        
        next_state = random.choices(next_state_keys, weights=next_state_probabilities, k=1)[0]
        
        return next_state

def distance(a, b):
    if not len(a) == len(b):
        raise Exception("A and B must have the same dimension")
    dim = len(a)
    if dim == 1:
        return np.abs(a - b)
    else:
        return np.sqrt(np.sum([(an - bn)**2 for an, bn in zip(a, b)]))

def to_hashable(obj):
    if isinstance(obj, np.ndarray):
        # Convert ndarray to a tuple of tuples (recursively hashable)
        return tuple(to_hashable(elem) for elem in obj)
    else:
        # Return the object itself if it is already hashable
        return obj