#João David - 89471
#Pedro Galhardo - 89522
#Grupo - 21

import math
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

	def __str__(self):
		return f"{self.positions}: {self.gcost}-{self.cost}"

	def __hash__(self):
		return hash((self.positions, self.tickets, self.goal))
	
	def __lt__(self, other):
		return self.gcost > other.gcost if self.cost == other.cost else self.cost < other.cost

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
		solution = deque()
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
		if anyorder:
			for goal in itertools.permutations(self.goal):
				heappush(open_nodes, Node(None, start_positions, [], tickets, goal, 0, self.distances))
		else:
			open_nodes.append(Node(None, start_positions, [], tickets, self.goal, 0, self.distances))

		closed_nodes = set()
		close_node = closed_nodes.add

		expansions = 0
		while open_nodes:
			node = heappop(open_nodes)

			if node in closed_nodes:
				continue
			close_node(node)

			if node.positions == node.goal:
				#print(f"Expansions: {expansions}")
				return self.traceback(node)

			if expansions  > limitexp or node.gcost > limitdepth:
				continue

			expansions += 1 #check this
			# Generate all possible from neighbours
			neighbours = [self.map[pos] for pos in node.positions]
			combinations = itertools.product(*neighbours)

			# Remove neighbours with agents on same position
			diff_positions = []
			for comb in combinations:
				occupy_same = False
				for i in range(self.n_agents):
					for j in comb[i+1:]:
						if comb[i][DEST] == j[DEST]:
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
					heappush(open_nodes, dest_node)

		return []
