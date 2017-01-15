"""
The MIT License (MIT)

Copyright (c) 2016 Eduardo Henrique Vieira dos Santos

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import neural, math, copy, random, pickle

class Gen:
	"""docstring for Gen
	This class is based on Genetic Algorithm to evolve a Network architecture to solve a given problem
	"""

	def __init__(self, name = "net"+str(random.random()), hIn = 1, hHi = 1, lHi = 1, hOu = 1, pSize = 50):
		self.name = name

		self.parent1 = None
		self.parent2 = None

		#Network architecture attributes
		self.heightInputLayer = hIn 	#qtty of neurons in first layer
		self.lenHiddenLayer = lHi 	#qtty of hidden layers
		self.heightHiddenLayer = hHi 	#qtty of neurons in each hidden layer
		self.heightOutputLayer = hOu 	#qtty of neurons in the output layer

		self.desiredInputs = []	#float list of inputs evaluated between 0 and 1
		self.desiredOutputs = []	#float list of its corresponding outputs evaluated between 0 and 1
		self.idealFitness = 0.001	#accetable miss, usually 1%
		self.mutationRate = 0.5	#mutation rate
		self.crossoverRate = 0.5
		self.populationSize = pSize	#population sizes
		self.population = []	#population of networks
		self.statistics = []
	
	def newRandom(self):
		#generates a newRandom Network with its neural espicifications
		net = neural.Network()
		net = net.newRandom(self.heightInputLayer, self.heightHiddenLayer, self.lenHiddenLayer, self.heightOutputLayer)
		net = self.mutation(net)
		return net

	def randomPopulate(self):
		#generates a new random population to be selected for first
		self.population = []
		for i in range(self.populationSize):
			self.population.append(self.newRandom())
		return True

	def populate(self, parent1, parent2, size):
		#generates a new population based on its size and parents
		newPopulation = []
		for i in range(size-2):
			net = neural.Network()
			net = self.crossover(parent1, parent2)
			net = self.mutation(net)
			newPopulation.append(net)
		newPopulation.append(parent1)
		newPopulation.append(parent2)
		self.population = newPopulation

	def crossover(self, net1, net2):
		#crossover between parents
		netA = copy.deepcopy(net1)
		netB = copy.deepcopy(net2)
		net = netA.newRandom(self.heightInputLayer,self.heightHiddenLayer,self.lenHiddenLayer,self.heightOutputLayer)

		for i in range(len(net.dendriteList)):
			for j in range(len(net.dendriteList[i].neuronList)):
				t = random.random()
				if t < self.crossoverRate:
					net.dendriteList[i].neuronList[j].weight = netA.dendriteList[i].neuronList[j].weight
					net.dendriteList[i].neuronList[j].bend = netA.dendriteList[i].neuronList[j].bend
				else:
					net.dendriteList[i].neuronList[j].weight = netB.dendriteList[i].neuronList[j].weight
					net.dendriteList[i].neuronList[j].bend = netB.dendriteList[i].neuronList[j].bend
				for k in range(len(net.dendriteList[i].neuronList[j].axon)):
					t = random.random()
					if t < self.crossoverRate:
						net.dendriteList[i].neuronList[j].axon[k].weight = netB.dendriteList[i].neuronList[j].axon[k].weight
						net.dendriteList[i].neuronList[j].axon[k].bend = netB.dendriteList[i].neuronList[j].axon[k].bend
		return net

	def mutation(self, net1):
		#apllies mutation over the network
		net = copy.deepcopy(net1)
		for i in net.dendriteList:
			if i != net.dendriteList[0]: #dodge first layer
				for j in i.neuronList:
					t = random.random()
					if t < self.mutationRate:
						j.randomize()
					for k in j.axon:
						t = random.random()
						if t < self.mutationRate:
							k.randomize()
		return net

	def rank(self, net):
		#Calculates the deviation between the Network Activation Outputs for each Desired Input to each Desired Output
		deviationSum = 0
		#Tests each Desired Inputs for each Desired Output
		for i in range(len(self.desiredInputs)):
			#Activates the Network with the Desired input
			z = net.activate(self.desiredInputs[i])
			#Compare each output...
			for j in range(len(z)):
				major = z[j]
				minor = float(self.desiredOutputs[i][j])
				#Compare the distance between the Network Outputs to the Desired Outputs
				distance = abs(major - minor)
				distance = distance**2
				if distance > self.idealFitness:
					#punishment if goal is not achieved
					distance = distance*1000*(len(self.desiredOutputs))#(len(self.desiredOutputs)*(math.sqrt(distance)) + 2) *( distance + len(self.desiredOutputs)*(math.sqrt(distance)*(math.e/2)))#(len(self.desiredOutputs)) + math.sqrt(distance)*(len(self.desiredOutputs))#
				deviationSum = deviationSum + distance
		return deviationSum

	def selection(self):
#		self.parent1 = None
#		self.parent2 = None
		for i in range(len(self.population)):
			
			rankI = self.rank(self.population[i])
			rank1 = float("inf")
			rank2 = float("inf")

			if self.parent1 is None:
				self.parent1 = self.population[i]
			if self.parent2 is None and self.population[i] != self.parent1:
				self.parent2 = self.population[i]

			if self.parent1 != None:
				rank1 = self.rank(self.parent1)
			if self.parent2 != None:
				rank2 = self.rank(self.parent2)

			if rankI < rank1:
				self.parent2 = self.parent1
				self.parent1 = self.population[i]

			if rankI > rank1 and rankI < rank2:
				self.parent2 = self.population[i]
#			if self.parent2 != None and self.rank(self.parent2) < self.rank(self.parent1):
#				aux = self.parent1
#				self.parent1 = self.parent2
#				self.parent2 = aux


	def evolve(self):
		#Evolve a Network to have its avoidance the minimal as possible

		#Generates a new random population
		self.randomPopulate()
		#Selects the better ones
		self.selection()

		#Shows the parents rank
		rank1 = self.rank(self.parent1)
		print "Parent1: ",rank1
		rank2 = self.rank(self.parent2)
		print "Parent2: ",rank2,"\n"

		#saves the present parents
		lastP1 = self.parent1
		lastP2 = self.parent2
		#sets lifetimecounter to 0
		lifetimeCounter = 0

		self.statistics.append([int(lifetimeCounter), rank1, rank2])

		#Loop for start the evolution process
		while  rank1 > self.idealFitness:

			#Generate a population with parents
			self.populate(self.parent1, self.parent2, self.populationSize)

			#Selection happens
			self.selection()

			print "|"+self.name+"|"

			if lastP1 == self.parent1:
				lifetimeCounter = lifetimeCounter + 1
				lastP1 = self.parent1
			else:
				lifetimeCounter = lifetimeCounter + 1
				self.statistics.append([int(lifetimeCounter), rank1, rank2])
				save("statistics-"+self.name,self.statistics)
				lastP1 = self.parent1

			if lastP2 == self.parent2:
				lifetimeCounter = lifetimeCounter + 1
				lastP2 = self.parent2
			else:
				lifetimeCounter = lifetimeCounter + 1
				self.statistics.append([int(lifetimeCounter), rank1, rank2])
				save("statistics-"+self.name,self.statistics)
				lastP2 = self.parent2

			print "||||||||||Parent2|||||||||"

			for i in range(len(self.desiredInputs)):
				z = self.parent2.activate(self.desiredInputs[i])
				print "Activation:\t",self.desiredInputs[i],"=",z
				print "Desired:\t",self.desiredInputs[i],"=",self.desiredOutputs[i]

			print "||||||||||Parent1|||||||||"

			#Displays each desired Inputs and its Outputs of the parents Network
			for i in range(len(self.desiredInputs)):
				z = self.parent1.activate(self.desiredInputs[i])
				print "Activation:\t",self.desiredInputs[i],"=",z
				print "Desired:\t",self.desiredInputs[i],"=",self.desiredOutputs[i]

			#Loading bar...
			print "Loading","."*(lifetimeCounter%30)
			print lifetimeCounter

			#Shows the parents Ranks on the screen
			rank1 = self.rank(self.parent1)
			print "Rank Parent1: ",rank1
			rank2 = self.rank(self.parent2)
			print "Rank Parent2: ",rank2

			#Overwrite and saves the data of the better parent at each cicle in case the script is interrupted
			self.parent1.save(self.name+".ann")

			if rank1 <= self.idealFitness:
				self.statistics.append([int(lifetimeCounter), rank1, rank2])
				save("statistics-"+self.name,self.statistics)
				lastP1 = self.parent1
				break

		self.parent1.save(self.name+".ann")

def save(name, ob):
	#save object
	pickle_out = open(name, "wb")
	pickle.dump(ob, pickle_out)
	pickle_out.close()

def load(name):
	pickle_in = open(name, "rb")
	z = pickle.load(pickle_in)
	pickle_in.close()
	return z


#Uncomment these lines to test a XOR and NXOR learning
#gen = Gen("XORXNOR", 2, 3, 2, 2)
#gen.populationSize = 50
#gen.desiredInputs = [[1,1],[1,0],[0,1],[0,0]]
#gen.desiredOutputs = [[0,1],[1,0],[1,0],[0,1]]
#gen.evolve()
