class State:
    def __init__(self, label, info):
        self.label = label
        self.info = info
        self.successors = []
    
    def add_successor(self, state):
        self.successors.append(state)
        
    def __hash__(self):
        return int(str(self.label[0]) + str(self.label[1]))
        
class Instance:
    def __init__(self):
        self.states = {}
        self.goal = None
        
    def set_goal(self, state):
        if state.info:
            self.goal = state
        else:
            raise ValueError("goal state is not reachable")
    
    def is_goal(self, state):
        return state.label == self.goal.label
        
    def add_state(self, i, j, free):
        self.states[(i, j)] = State((i, j), free)
        
    def add_successor(self, i, j, p, q):
        self.states[(i, j)].add_successor(self.states[(p, q)])

