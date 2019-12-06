#Joao Carlos Morgado David - 89471
#Pedro Miguel da Silva Galhardo - 89522
#Grupo - 21

import random
from numpy import inf

class LearningAgent:

	# nS maximum number of states
	# nA maximum number of action per state
	def __init__(self,nS,nA):
		self.nS = nS
		self.nA = nA
		self.Q = [[-inf] * nA for s in range(nS)]
		self.N = [[0] * nA for s in range(nS)]
		self.alpha = 0.65
		self.gamma = 0.8
		self.epsilon = 1

	def explore(self, st, aa):
		# Choose randomly between less frequently picked
		min_N = min(self.N[st][:len(aa)])
		indexes = []
		for i in range(len(aa)):
			if self.N[st][i] == min_N:
				indexes.append(i)
		
		return random.choice(indexes)
	
	def exploit(self, st, aa):
		# Use max_Q
		max_Q = max(self.Q[st][:len(aa)])
		indexes = []
		for i in range(len(aa)):
			if self.Q[st][i] == max_Q:
				indexes.append(i)
		
		return random.choice(indexes)

	# Select one action, used when learning  
	# st - is the current state        
	# aa - is the set of possible actions
	# for a given state they are always given in the same order
	# returns
	# a - the index to the action in aa
	def selectactiontolearn(self,st,aa):
		if all(e == -inf for e in self.Q[st]):
			for i in range(len(aa)):
				self.Q[st][i] = 0

		choice = self.exploit(st, aa) if (random.random() > self.epsilon) else self.explore(st,aa)
		self.N[st][choice] += 1

		# Gradually enable exploiting using max_Q
		if self.epsilon > 0.10:
			self.epsilon -= 0.01

		return choice

	# Select one action, used when evaluating
	# st - is the current state        
	# aa - is the set of possible actions
	# for a given state they are always given in the same order
	# returns
	# a - the index to the action in aa
	def selectactiontoexecute(self,st,aa):
		return self.exploit(st, aa)

	# this function is called after every action
	# ost - original state
	# nst - next state
	# a - the index to the action taken
	# r - reward obtained
	def learn(self,ost,nst,a,r):
		max_Q =  0
		if any(e != -inf for e in self.Q[nst]):
			max_Q = max(self.Q[nst])

		self.Q[ost][a] = self.Q[ost][a] + self.alpha * (r + (self.gamma * max_Q) - self.Q[ost][a])
