import math
import pickle
import time
from collections import deque
import itertools
import functools
from heapq import heappush, heappop

TAXI = 0
AUTOCARRO = 1
METRO = 2

TRANSPORT = 0
DEST = 1

class Node:
  def __init__(self, origin_node, positions, transports, tickets, g):
    self.origin_node = origin_node
    self.positions = tuple(positions)
    self.transports = transports
    self.tickets = tuple(tickets)
    self.gcost = self.cost = g

  def calculate_cost(self, goal, coords):
    def get_coords(pos):
      return coords[pos-1]

    for i in range(len(goal)):
      self.cost += ((get_coords(self.positions[i])[0] - get_coords(goal[i])[0])**2 +
                    (get_coords(self.positions[i])[1] - get_coords(goal[i])[1])**2)
    


  def __repr__(self):
    return f"({self.transports}, {self.positions}, {self.tickets})"
  
  def __hash__(self):
    return hash((self.positions, self.tickets))
  
  def __lt__(self, other):
    return self.cost < other.cost

  def __eq__(self, other):
    if (other == None):
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
      solution.appendleft([list(current_node.transports), list(current_node.positions)])
      current_node = current_node.origin_node
    
    return list(solution)

  def Astar(self, init, goal, tickets):
    num_agents = len(init)

    init_node = Node(None, init[:], [], tickets, 0)
    init_node.calculate_cost(goal, self.coords)

    open_nodes = [init_node]

    closed_nodes = set()
    close_node = closed_nodes.add

    while open_nodes:
      node = heappop(open_nodes)

      # Even if it's closed the node might have been added twice (or more)
      # It's not worth checking if the node is in open_nodes when adding
      # because that would take time O(n)
      #print(closed_nodes)
      if node in closed_nodes:
        continue
      close_node(node)

      
      if node.positions == tuple(goal): # same order comparison
        return self.traceback(node)

      # Generate all possible from neighbours
      neighbours = [self.map[pos] for pos in node.positions]
      combinations = itertools.product(*neighbours)

      # Remove neighbours with agents on same position
      diff_positions = []
      for comb in combinations:
        found = False
        for i in range(num_agents):
          for j in range(i + 1, num_agents):
              if comb[i][DEST] == comb[j][DEST]:
                found = True
                break
        if not found:
          diff_positions.append(comb)

      for dest in diff_positions:
        new_tickets = list(node.tickets)
        out_of_tickets = False
        for movement in dest:
          new_tickets[movement[TRANSPORT]] -= 1
          if new_tickets[movement[TRANSPORT]] < 0:
            out_of_tickets = True

          if not out_of_tickets:
            dest_node = Node(node, [path[DEST] for path in dest], [path[TRANSPORT] for path in dest],
                             new_tickets, node.gcost+ 1)
            if dest_node not in closed_nodes:
              dest_node.calculate_cost(goal, self.coords)
              #if dest_node not in open_nodes: # Ou o caminho é melhor, se o caminho for melhor é trocar
              heappush(open_nodes, dest_node) # Inserir ordenado

    return []


  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyOrder = false):
    res = self.Astar(init, self.goal, tickets)
    print(res)
    return res
