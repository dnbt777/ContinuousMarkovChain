import random


class ContinuousMarkovChain():
    def __init__(self, sequences*):       
        self.chain_states = {} # init the chain
        self.sequences = sequences # store seqs in case I need em later
        for seq in sequences:
            self.populate_chain_states(seq) # update chain w sequences
    
    
    def populate_chain_states(self, seq):
        for i, element in enumerate(seq):
            if i == len(seq):
                future_state = None
            else:
                future_state = self.seq[i+1]
            
            self.update_chain_state(element, future_state)
            
    
    def update_chain_state(element, future_state):
        if element in self.chain_states:
            self.chain_states[element].append(future_state)
        else:
            self.chain_states.update({element : [future_state]})
    
    
    def get_next_state(self, current_state):
        # current state does NOT NEED TO BE IN SEQ AT ALL!!!!!!!!!!!!!!!!!!!!!!!!!!!! WTHAT?!?!?!?!
        idx, state_info = enumerate(chain_states.items())
        elements, next_states = state_info
        
        distances = [abs(current_state - elem) for elem in elements] # precompute this
        weights = [1/(r**2) for r in distances] # multiply by no. of future states? i.e. if a state has 4 future states (NO that isnt logical)
        
        probability_distribution = weights/sum(weights)
        
        next_state = random.choice(next_states, p=probability_distribution)
        
        return next_state
        
        