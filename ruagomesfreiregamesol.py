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
  def __init__(self, origin_node, positions, transports, tickets, g):
    self.origin_node = origin_node
    self.positions = tuple(positions)
    self.transports = transports
    self.tickets = tuple(tickets)
    self.gcost = self.cost = g

  def calculate_ordered(self, goal, distances):
    return min(self.calculate_unordered(goal_i, distances) for goal_i in goal)

  def calculate_unordered(self, goal, distances):
    return self.cost + max(distances[goal][i] for i in self.positions)

  def __hash__(self):
    return hash((self.positions, self.tickets))
  
  def __lt__(self, other):
    return self.cost < other.cost

  def __eq__(self, other):
    if other == None:
      return False

    return (self.positions == other.positions and
            self.tickets == other.tickets)


class SearchProblem:

  def __init__(self, goal, model, auxheur = []):
    self.map = model
    self.goal = tuple(goal)
    self.n_agents = len(goal)
    self.distances = {}
    self.calc_distances()

  def traceback(self, dest):
    current_node = dest
    solution =  deque()
    while current_node != None:
      solution.appendleft([list(current_node.transports), list(current_node.positions)])
      current_node = current_node.origin_node
    
    return list(solution)

  def ordered_goal(self, node):
    return node.positions == self.goal

  def unordered_goal(self, node):
    return set(node.positions) == set(self.goal)

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

    goal_achieved = self.unordered_goal if anyorder else self.ordered_goal
    calculate_cost = Node.calculate_unordered if anyorder else Node.calculate_ordered
    if anyorder: self.goal = itertools.permutations(self.goal)

    init_node = Node(None, init[:], [], tickets, 0)

    open_nodes = [init_node]

    closed_nodes = set()
    close_node = closed_nodes.add

    while open_nodes:
      node = heappop(open_nodes)

      # Even if it's closed the node might have been added more than once
      # but we're sure the cost is worse because it has been already picked
      # from the queue. It's not worth checking if the node is in open_nodes
      # when adding because that would take time O(n) since open_nodes is a priority queue
      # This if can be done because for two nodes to be the same they have to occupy the same
      # positions on the map with the same number of available tickets
      if node in closed_nodes:
        continue
      close_node(node)

      if goal_achieved(node):
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
                           new_tickets, node.gcost+ 1)
    #      if dest_node not in closed_nodes: # Check if this if is worth
          dest_node.cost = calculate_cost(dest_node, self.goal, self.distances)
          heappush(open_nodes, dest_node)

    return []
