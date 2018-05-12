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
        try:
            self.goal = self.states[state]
        except:
            raise InvalidGoalError("goal state is not reachable")
    
    def is_goal(self, state):
        return state.label == self.goal.label
        
    def add_state(self, i, j, free):
        self.states[(i, j)] = State((i, j), free)
        
    def add_successor(self, i, j, p, q, cost):
        self.states[(i, j)].add_successor((self.states[(p, q)], cost))

class Node:
    def __init__(self, state, pred = None, cost = 0, depth = 0):
        self.state = state
        self.pred = pred
        self.cost = cost
        self.depth = depth
        
    def __lt__(self, other):
        return self.cost < other.cost
        
    def __gt__(self, other):
        return self.cost > other.cost
        
    def __str__(self):
        return "<%d %d %g>" % (self.state.label[0], self.state.label[1], self.cost)

class Solution:
    def __init__(self, goal, open_list, closed_list):
        self.steps = []
        self.info = {}
        
        self.info["nodes_generated"] = open_list.nodes()
        self.info["nodes_expanded"] = closed_list
        self.info["depth"] = goal.depth
        self.info["cost"] = goal.cost
        i = goal
        
        while i:
            self.steps.append(i)
            i = i.pred
            
        self.steps.reverse()
        
        self.info["b*"] = len(self.info["nodes_generated"]) ** (1 / self.info["depth"])
        
    def __getitem__(self, key):
        return self.steps[key]
            
    def __str__(self):
        return " ".join(list(map(lambda s: "<%d, %d, %g>" % (s.state.label[0], s.state.label[1], s.cost), self.steps)))

class SolutionNotFoundError(Exception):
    def __init__(self, open_list, closed_list):
        self.open_list = open_list
        self.closed_list = closed_list

class InvalidGoalError(Exception):
    def __init__(self, message):
        super().__init__(message)

class ManhattanDistanceHeuristic:
    def __init__(self, goal):
        self.goal = goal
    
    def get(self, node):
        dx = abs(node.state.label[0] - self.goal[0])
        dy = abs(node.state.label[1] - self.goal[1])
        
        return dx + dy

class OctileDistanceHeuristic:
    def __init__(self, goal):
        self.goal = goal
        
    def get(self, node):
        dx = abs(node.state.label[0] - self.goal[0])
        dy = abs(node.state.label[1] - self.goal[1])
        
        return max(dx, dy) + 0.5 * min(dx, dy)

class OpenList(object):
    def __init__(self):
        self.nodes_generated = set()
        
    def init(self, nodes):
        self.nodes_generated = set(nodes)
        
    def extend(self, nodes):
        for node in nodes:
            self.nodes_generated.add(node)
        
    def nodes(self):
        return self.nodes_generated

class BreadthFirstOpenList(OpenList):
    def __init__(self):
        super().__init__()
        self.open_list = deque([])
        
    def __str__(self):
        return str(list(map(str, self.open_list)))
        
    def __len__(self):
        return len(self.open_list)
        
    def init(self, nodes):
        super().init(nodes)
        self.open_list = deque(list(nodes))
        
    def pop(self):
        return self.open_list.popleft()
        
    def extend(self, nodes):
        super().extend(nodes)
        self.open_list.extend(nodes)
        
class UniformCostOpenList(OpenList):
    def __init__(self):
        super().__init__()
        self.open_list = []
            
    def __str__(self):
        return str(list(map(str, map(lambda n: n[1], self.open_list))))
        
    def __len__(self):
        return len(self.open_list)
        
    def init(self, nodes):
        super().init(nodes)
        self.open_list = []
        
        for node in nodes:
            heapq.heappush(self.open_list, (node.cost, node))
        
    def pop(self):
        return heapq.heappop(self.open_list)[1]
        
    def extend(self, nodes):
        super().extend(nodes)
        
        for node in nodes:
            heapq.heappush(self.open_list, (node.cost, node))

class LimitedDepthFirstOpenList(OpenList):
    def __init__(self, limit):
        super().__init__()
        self.limit = limit
        self.open_list = []
        
    def __str__(self):
        return str(list(map(str, self.open_list)))
        
    def __len__(self):
        return len(self.open_list)
        
    def init(self, nodes):
        super().init(list(filter(lambda n: n.cost <= self.limit, nodes)))
        self.open_list = [] + list(filter(lambda n: n.cost <= self.limit, nodes))
        
    def pop(self):
        return self.open_list.pop()
        
    def extend(self, nodes):
        super().extend(filter(lambda n: n.cost <= self.limit, nodes))
        self.open_list.extend(filter(lambda n: n.cost <= self.limit, nodes))

class BestFirstOpenList(OpenList):
    def __init__(self, heuristic):
        super().__init__()
        self.open_list = []
        self.heuristic = heuristic
            
    def __str__(self):
        return str(list(map(str, map(lambda n: n[1], self.open_list))))
        
    def __len__(self):
        return len(self.open_list)
        
    def init(self, nodes):
        super().init(nodes)
        self.open_list = []
        
        for node in nodes:
            heapq.heappush(self.open_list, (self.heuristic.get(node), node))
        
    def pop(self):
        return heapq.heappop(self.open_list)[1]
        
    def extend(self, nodes):
        super().extend(nodes)
        
        for node in nodes:
            heapq.heappush(self.open_list, (self.heuristic.get(node), node))

class AStarOpenList(OpenList):
    def __init__(self, heuristic):
        super().__init__()
        self.open_list = []
        self.heuristic = heuristic
            
    def __str__(self):
        return str(list(map(str, map(lambda n: n[1], self.open_list))))
        
    def __len__(self):
        return len(self.open_list)
        
    def init(self, nodes):
        super().init(nodes)
        self.open_list = []
        
        for node in nodes:
            heapq.heappush(self.open_list, (node.cost + self.heuristic.get(node), node))
        
    def pop(self):
        return heapq.heappop(self.open_list)[1]
        
    def extend(self, nodes):
        super().extend(nodes)
        
        for node in nodes:
            heapq.heappush(self.open_list, (node.cost + self.heuristic.get(node), node))

def search(instance, start, open_list):
    closed_list = set()
    best_path = {}
    open_list.init([Node(instance.states[start])])
    
    while open_list:
        current = open_list.pop()
        
        if instance.is_goal(current.state):
            return Solution(current, open_list, closed_list)
            
        if current.state.label not in closed_list or current.cost < best_path[current.state.label]:
            closed_list.add(current.state.label)
            
            best_path[current.state.label] = current.cost
            
            open_list.extend(list(map(lambda s: Node(s[0], current, current.cost + s[1], current.depth + 1), 
                                        current.state.successors)))
    
    raise SolutionNotFoundError(open_list, closed_list)