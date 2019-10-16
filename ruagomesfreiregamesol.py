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

  def calculate_ordered(self, goal, coords):
    def get_coords(pos):
      return coords[pos-1]

    for i in range(len(goal)):
      self.cost += ((get_coords(self.positions[i])[0] - get_coords(goal[i])[0])**2 +
                    (get_coords(self.positions[i])[1] - get_coords(goal[i])[1])**2)

  def calculate_unordered(self, goal, coords):
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
    self.goal = tuple(goal)
    self.coords = auxheur

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

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):

    TRANSPORT, DEST = 0, 1
    num_agents = len(init)

    goal_achieved = self.unordered_goal if anyorder else self.ordered_goal
    calculate_cost = Node.calculate_unordered if anyorder else Node.calculate_ordered

    init_node = Node(None, init[:], [], tickets, 0)
    calculate_cost(init_node, self.goal, self.coords)

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
        for i in range(num_agents):
          for j in range(i + 1, num_agents):
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
          calculate_cost(dest_node, self.goal, self.coords)
          heappush(open_nodes, dest_node)

    return []
