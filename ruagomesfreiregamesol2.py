#João David - 89471
#Pedro Galhardo - 89522
#Grupo - 21

import math
import pickle
import time
from collections import deque
import itertools
from heapq import heappush, heappop

class Node:
  def __init__(self, origin_node, positions, transports, tickets, goal, gcost, distances):
    self.origin_node = origin_node
    self.positions = tuple(positions)
    self.transports = transports
    self.tickets = tuple(tickets)
    self.goal = goal
    self.gcost = gcost
    self.cost = gcost + max(distances[goal[i]][positions[i]] for i in range(len(positions)))


  def calculate_h(self, goal, distances):
    self.cost += max(distances[goal][i] for i in self.positions)

  def __str__(self):
    return f"{self.positions}: {self.cost}"

  def __hash__(self):
    return hash((self.positions, self.tickets, self.goal))
  
  def __lt__(self, other):
    return self.cost < other.cost

  def __eq__(self, other):
    if other == None:
      return False

    return (self.positions == other.positions and
            self.tickets == other.tickets and
            self.goal == other.goal)


class SearchProblem:

  def __init__(self, goal, model, auxheur = []):
    self.map = model
    self.goal = tuple(goal)
    self.n_agents = len(goal) #testar sem guardar isto
    self.distances = {}
    self.calc_distances()

  def traceback(self, dest):
    current_node = dest
    solution =  deque()
    while current_node != None:
      solution.appendleft([list(current_node.transports), list(current_node.positions)])
      current_node = current_node.origin_node
    
    return list(solution)

  def calc_distances(self):
    DEST = 1
    n_nodes = len(self.map)
    
    for start in self.goal:
      distances = [-1] * n_nodes
      distances[start] = 0

      frontier = [start]
      next = frontier.pop
      add_node = frontier.append

      while frontier != []:
        node = next(0)

        for path in self.map[node]:
          dest = path[DEST]

          if distances[dest] == -1 and dest not in frontier:
            distances[dest] = distances[node] + 1
            add_node(dest)

      self.distances[start] = distances

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
    TRANSPORT, DEST = 0, 1

    open_nodes = []

    start_positions = init[:]
    for goal in itertools.permutations(self.goal):
      heappush(open_nodes, Node(None, start_positions, [], tickets, goal, 0, self.distances))

    closed_nodes = set()
    close_node = closed_nodes.add

    while open_nodes:
      node = heappop(open_nodes)

      if node in closed_nodes:
        continue
      close_node(node)

      if node.positions == node.goal:
        return self.traceback(node)

      # Generate all possible from neighbours
      neighbours = [self.map[pos] for pos in node.positions]
      combinations = itertools.product(*neighbours)

      # Remove neighbours with agents on same position
      diff_positions = []
      for comb in combinations:
        occupy_same = False
        for i in range(self.n_agents):
          for j in range(i + 1, self.n_agents):
              if comb[i][DEST] == comb[j][DEST]:
                occupy_same = True
                break
        if not occupy_same:
          diff_positions.append(comb)

      for dest in diff_positions:
        new_tickets = list(node.tickets)
        out_of_tickets = False
        for move in dest:
          new_tickets[move[TRANSPORT]] -= 1
          if new_tickets[move[TRANSPORT]] < 0:
            out_of_tickets = True

        if not out_of_tickets:
          dest_node = Node(node, [path[DEST] for path in dest], [path[TRANSPORT] for path in dest],
                           new_tickets, node.goal, node.gcost + 1, self.distances)
          #if dest_node not in closed_nodes: # Check if this if is worth
          heappush(open_nodes, dest_node)

    return []
