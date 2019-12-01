import random
import os
import sys

class LearningAgent:

	# nS maximum number of states
	# nA maximum number of action per state
	def __init__(self,nS,nA):

		self.nS = nS
		self.nA = nA
		self.Q = [[-5] * nA for s in range(nS)]
		self.alpha = float(sys.argv[1])
		self.gamma = float(sys.argv[2])
	
	def exploit(self, st, aa):
		return self.Q[st].index(max(self.Q[st]))

	def explore(self, st, aa):
		choice = random.choice(range(len(aa)))
		return choice

	# Select one action, used when learning  
	# st - is the current state        
	# aa - is the set of possible actions
	# for a given state they are always given in the same order
	# returns
	# a - the index to the action in aa
	def selectactiontolearn(self,st,aa):
		# explore %
		self.last_len = len(aa)
		return self.explore(st, aa)

	# Select one action, used when evaluating
	# st - is the current state        
	# aa - is the set of possible actions
	# for a given state they are always given in the same order
	# returns
	# a - the index to the action in aa
	def selectactiontoexecute(self,st,aa):
		self.last_len = len(aa)
		return self.exploit(st, aa)

	# this function is called after every action
	# ost - original state
	# nst - next state
	# a - the index to the action taken
	# r - reward obtained
	def learn(self,ost,nst,a,r):
		self.Q[ost][a] = self.Q[ost][a] + self.alpha * (r + (self.gamma*max(self.Q[nst])) - self.Q[ost][a])
