import math
import pickle
import time
from collections import deque
import itertools
import functools

TAXI = 0
AUTOCARRO = 1
METRO = 2

TRANSPORT = 0
DEST = 1

class Node:
  def __init__(self, origin_node, positions, transports, tickets):
    self.origin_node = origin_node
    self.positions = positions
    self.transports = transports
    self.tickets = tickets

  def __repr__(self):
    return f"({self.transports}, {self.positions})"
  
  def __hash__(self):
    return hash((tuple(self.positions), tuple(self.tickets)))
  
  def __eq__(self, other):
    if other == None:
      return False

    return (self.positions == other.positions and
            self.tickets == other.tickets)

class SearchProblem:

  def __init__(self, goal, model, auxheur = []):
    self.map = model
    self.goal = goal
    self.coords = auxheur

  def traceback(self, dest):
    current_node = dest
    solution =  deque() #  Comparar velocidades com listas
    while current_node != None:
      solution.appendleft([current_node.transports, current_node.positions])
      current_node = current_node.origin_node
    
    return list(solution)

  def Astar(self, init, goal, tickets):
    num_agents = len(init)

    init_node = Node(None, init[:], [], tickets)
    open_nodes = deque([init_node]) # double linked list
    open_node = open_nodes.append

    closed_nodes = set()
    close_node = closed_nodes.add

    get_next = open_nodes.popleft
    while open_nodes:
      node = get_next()
      close_node(node)

      
      if node.positions == goal: # same order comparison
        return self.traceback(node)

      # generate all possible combinations
      reachable = [self.map[pos] for pos in node.positions]
      combinations = itertools.product(*reachable)

      unique = []
      for comb in combinations:
        found = False
        for i in range(num_agents):
          for j in range(i + 1, num_agents):
              if comb[i][DEST] == comb[j][DEST]:
                found = True
                break
        if not found:
          unique.append(comb)

      print("uniq:", unique)
      for i in range(num_agents):
        
        for path in self.map[node.positions[i]]:
          new_tickets = node.tickets[:]
          transports = []

          if node.tickets[path[TRANSPORT]] > 0:
            new_tickets[path[TRANSPORT]] -= 1
            dest = path[DEST]
            #print(f"To: ({path[TRANSPORT]}, {dest})")
            dest_node = Node(node, dest, transports, new_tickets)

            if dest_node not in closed_nodes:  
              if dest_node not in open_nodes: # Ou o caminho é melhor, se o caminho for melhor é trocar
                open_node(dest_node) # Inserir ordenado

    return []


  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf]):
    res = self.Astar(init, self.goal, tickets)
    print(res)
    return res
