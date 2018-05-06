from collections import deque
import heapq

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
        
    def add_successor(self, i, j, p, q, cost):
        self.states[(i, j)].add_successor((self.states[(p, q)], cost))

class Node:
    def __init__(self, state, pred = None, cost = 0):
        self.state = state
        self.pred = pred
        self.cost = cost
        
    def __lt__(self, other):
        return self.cost < other.cost
        
    def __gt__(self, other):
        return self.cost > other.cost
        
    def __str__(self):
        return "<%d %d %g>" % (self.state.label[0], self.state.label[1], self.cost)

class Solution:
    def __init__(self, goal):
        self.steps = []
        i = goal
        
        while i.pred:
            self.steps.append(i)
            i = i.pred
            
        self.steps.reverse()
            
    def __str__(self):
        return " ".join(list(map(lambda s: "<%d, %d, %g>" % (s.state.label[0], s.state.label[1], s.cost), self.steps)))

class SolutionNotFoundError(Exception):
    pass

class BreadthFirstOpenList:
    def __init__(self, nodes):
        self.open_list = deque(nodes)
        
    def __str__(self):
        return str(list(map(str, self.open_list)))
        
    def pop(self):
        return self.open_list.popleft()
        
    def extend(self, nodes):
        self.open_list.extend(nodes)
        
class UniformCostOpenList:
    def __init__(self, nodes):
        self.open_list = []
        
        for node in nodes:
            heapq.heappush(self.open_list, (node.cost, node))
            
    def __str__(self):
        return str(list(map(str, map(lambda n: n[1], self.open_list))))
        
    def pop(self):
        return heapq.heappop(self.open_list)[1]
        
    def extend(self, nodes):
        for node in nodes:
            heapq.heappush(self.open_list, (node.cost, node))

def search(instance, start, open_list_builder):
    closed_list = set()
    open_list = open_list_builder([Node(instance.states[start])])
    
    while open_list:
        current = open_list.pop()
        
        if instance.is_goal(current.state):
            return Solution(current)
            
        if current.state not in closed_list:
            closed_list.add(current.state)
            open_list.extend(map(lambda s: Node(s[0], current, current.cost + s[1]), current.state.successors))
        
    raise SolutionNotFoundError()