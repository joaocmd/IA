import math
import pickle
import time
from enum import Enum

TAXI = 0
AUTOCARRO = 1
METRO = 2

TRANSPORT = 0
DEST = 1

class BFSNode:
  def __init__(self, id, origin_node, transport, tickets):
    self.id = id
    self.origin_node = origin_node
    self.transport = transport
    self.tickets = tickets 

  def __repr__(self):
    return f"({self.transport}, {self.id})"


class SearchProblem:

  def __init__(self, goal, model, auxheur = []):
    self.map = model
    self.goal = goal

  def traceback(self, dest):
    current_node = dest
    solution =  []
    while current_node != []:
      transports = [] if current_node.transport == None else [current_node.transport]
      solution.insert(0, [transports, [current_node.id]])
      current_node = current_node.origin_node
    
    return solution
      
  def in_frontier(self, frontier, id):
    for node in frontier:
      if node.id == id:
        return True

    return False

  def BFS(self, init, goal, tickets):

    nodes = [None] * 114     # node list
    nodes[init[0]] = BFSNode(init[0], [], None, tickets) 

    explored = [False] * 114 # bool list
    frontier = [nodes[init[0]]]     # node list

    while frontier != []:
      node = frontier.pop(0)
      explored[node.id] = True
      print(f"-----------------EXPANDING-----------------")
      print(f"From: {node.id}")
      print(self.map[node.id])
      
      for path in self.map[node.id]:
        dest = path[DEST]
        print(f"To: ({path[TRANSPORT]}, {dest})")
        if not explored[dest] and not self.in_frontier(frontier, dest) and node.tickets[path[TRANSPORT]] > 0: #O(n)
          new_tickets = node.tickets[:] 
          new_tickets[path[TRANSPORT]] -= 1
          nodes[dest] = BFSNode(dest, node, path[TRANSPORT], new_tickets)
          if dest == goal[0]: # reached goal, traceback
            return self.traceback(nodes[dest])
            
          frontier.append(nodes[dest])

    return []


  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf]):
    return self.BFS(init, self.goal, tickets)
