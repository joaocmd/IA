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
		#self.alpha = float(sys.argv[1])
		#self.gamma = float(sys.argv[2])
		self.alpha = 0.7
		self.gamma = 0.8
	
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

		#Choose randomly between less frequently picked
		min_N = min(self.N[st][:len(aa)])
		indexes = []	
		for i in range(len(aa)):
			if self.N[st][i] == min_N:
				indexes.append(i)
		choice = random.choice(indexes)
		self.N[st][choice] += 1

		return choice

	# Select one action, used when evaluating
	# st - is the current state        
	# aa - is the set of possible actions
	# for a given state they are always given in the same order
	# returns
	# a - the index to the action in aa
	def selectactiontoexecute(self,st,aa):
		return self.Q[st].index(max(self.Q[st][:len(aa)]))

	# this function is called after every action
	# ost - original state
	# nst - next state
	# a - the index to the action taken
	# r - reward obtained
	def learn(self,ost,nst,a,r):
		max_Q =  0
		if any(e != -inf for e in self.Q[nst]):
			max_Q = max(self.Q[nst])

		self.Q[ost][a] = self.Q[ost][a] + self.alpha * (r + (self.gamma*max_Q) - self.Q[ost][a])
