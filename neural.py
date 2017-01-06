#encoding: utf-8
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
import math, random, pickle

class Neuron:
	"""docstring for Neuron
		It represents a Neuron processing unity
	"""
	def __init__(self, input = [], bend = 0, weight = 1, axon = [], output = 0):
		if bend > 0.5:	#Controls the direction of the sigmoid function
			self.bend = 1	#descending	^\_
		else:
			self.bend = -1	#ascending	_/^
		self.weight = weight
		self.input = input
		self.output = output
		self.axon = axon

	def randomize(self):
		z = random.random()
		if z > 0.5:
			self.bend = 1
		else:
			self.bend = -1
		z = random.random()
		self.weight = z

	def addInput(self, i):
		self.input.append(i)

	def activate(self):
		junc = 1 / ( 1 + 10**( -1 * math.e * ( sum(self.input) * 2-1) ) )
		self.output = 1 / ( 1 + 10**( self.bend * math.e * ( junc * 2-1) ) )
		return self.output

	def addConnection(self, target, bend = 0, weight = 1):
		if bend > 0.5:
			bend = 1
		else:
			bend = -1
		if len(self.axon) < 1:
			ax = AxonTerminal(bend, weight)
			ax.input = self
			ax.output = target
			self.axon = [ax]
			return self.axon
		else:
			ax = AxonTerminal(bend, weight)
			ax.input = self
			ax.output = target
			self.axon.append(ax)
			return self.axon

	def communicate(self):
		for i in self.axon:
			i.setOutput()
		return self.axon

class AxonTerminal:
	"""docstring for AxonTerminal
		It represents a terminal connection between neuron A and B
	"""
	def __init__(self, bend = 0, weight = 1, input = Neuron(), output = Neuron()):
		if bend > 0.5:
			self.bend = 1
		else:
			self.bend = -1
		self.weight = weight
		self.input = input
		self.output = output

	def randomize(self):
		z = random.random()
		if z > 0.5:
			self.bend = 1
		else:
			self.bend = -1
		z = random.random()
		self.weight = z

	def setOutput(self):
		self.output.input.append(1 / ( 1 + 10**( self.bend * math.e * ( self.weight * self.input.output * 2-1) ) ))

class Dendrite:
	"""docstring for Dendrite
		It represents a layer of neurons
	"""
	def __init__(self, neuronList = [], output = []):
		self.neuronList = neuronList
		self.output = output

	def newRandomNeurons(self, qtNeurons):
		nList = []
		for i in range(qtNeurons):
			n = Neuron()
			nList.append(n)
		return nList

	def addRandomConnection(self, target):
		for i in self.neuronList:
			for j in target.neuronList:
				i.addConnection(j, random.random(), random.random())

	def addConnection(self, target):
		for i in self.neuronList:
			for j in target.neuronList:
				i.addConnection(j)

	def activate(self):
		for i in self.neuronList:
			i.activate()

	def communicate(self):
		for i in self.neuronList:
			i.communicate()

	def injectInput(self, input):
		if len(input) == len(self.neuronList):
			for i in range(len(self.neuronList)):
				self.neuronList[i].addInput(input[i])
			return True
		else:
			return False

	def clearIO(self):
		self.output = []
		if len(self.neuronList) > 0:
			for i in (self.neuronList):
				i.input = []
				i.output = []
			return True
		else:
			return False

	def setOutput(self):
		for i in self.neuronList:
			self.output.append(i.output)
		return self.output
		
class Network:
	"""docstring for Dendrite
		It represents a layer of neurons
	"""
	def __init__(self, dendriteList = [], input = [], output = []):
		self.input = input
		self.dendriteList = dendriteList
		self.output = output


	def newRandom(self, inputHeight, hiddenHeight, hiddenWidth, outputHeight):
		dendriteList = []
		nList = []
		for i in range(inputHeight):
			n = Neuron([],0,1)
			nList.append(n)
		dendriteList.append(Dendrite(nList))

		for i in range(hiddenWidth):
			nListh = []
			for i in range(hiddenHeight):
				n = Neuron()
				n.randomize
				nListh.append(n)
			dendriteList.append(Dendrite(nListh))
		nListO = []
		for i in range(outputHeight):
			n = Neuron()
			n.randomize
			nListO.append(n)
		dendriteList.append(Dendrite(nListO))

		for i in range(1, len(dendriteList)):
			dendriteList[i-1].addRandomConnection(dendriteList[i])
		net = Network(dendriteList)
		return net
	
	def save(self, name):
		#Save the present Network using pickle
		pickle_out = open(name, "wb")
		pickle.dump(self, pickle_out)
		pickle_out.close()

	def load(self, name):
		#Load another Network set using pickle
		pickle_in = open(name, "rb")
		z = pickle.load(pickle_in)
		pickle_in.close()
		return z

	def activate(self, input):
		for i in self.dendriteList:
			i.clearIO()
		self.input = input
		self.injectInput(self.input)
		for i in self.dendriteList:
			i.activate()
			i.communicate()
		return self.setOutput()

	def injectInput(self, input):
		self.dendriteList[0].injectInput(input)

	def clearIO(self):
		self.output = []
		for i in (self.dendriteList):
			i.clearIO()
		return True

	def setOutput(self):
		self.output = []
		if self.dendriteList > 0:
			self.dendriteList[-1].setOutput()
			self.output = self.dendriteList[-1].output
			return self.output
		
	def show(self):
		for i in self.dendriteList:
			print i,"\n HAS :"
			for j in i.neuronList:
				print "\n\tNEURON :",j,"\n\t WITH LINKs "
				for k in j.axon:
					print "\t\t",k,"\n\t\t\t TO ",k.output

			print "_________________________________"


#TESTS



#Perceptron:



#Simple AND
#______________________________________________________
"""
#print "Neurons"
x1 = Neuron()
x2 = Neuron()
y1 = Neuron()
y2 = Neuron()

print x1.axon
print x1.addConnection(y1, 0, 0.5)
print x2.axon
print x2.addConnection(y1, 0, 0.5)

print x1.axon
print x1.addConnection(y2, 0, 0.6)
print x2.axon
print x2.addConnection(y2, 0, 0.6)

#NEURONS ONLY
#print x1.activate()
#print x2.activate()
#print x1.communicate()
#print x2.communicate()

#print y1.activate()
#print y2.activate()
#WITH DENDRITES
layer1 = Dendrite([x1,x2])
layer2 = Dendrite([y1,y2])

#layer1.activate()
#layer1.communicate()
#layer2.activate()
#layer2.communicate()
#print layer2.setOutput()

#WITH NETWORK
net = Network([layer1,layer2])
net.clearIO()
print net.activate([1,1])
print net.activate([0,1])
print net.activate([1,0])
print net.activate([0,0])


#______________________________________________________



#Simple OR
#______________________________________________________

#print "Neurons"
#x1 = Neuron([1])
#x2 = Neuron([1])
#y = Neuron()

#print x1.axon
#print x1.addConnection(y, 0, 0.6)

#print x2.axon
#print x2.addConnection(y, 0, 0.6)

#WITH DENDRITES
#layer1 = Dendrite([x1,x2])
#layer2 = Dendrite([y])

#layer1.activate()
#layer1.communicate()
#layer2.activate()
#layer2.communicate()
#print layer2.setOutput()

#WITHOUT DENDRITES
#print x1.activate()
#print x2.activate()
#print x1.communicate()
#print x2.communicate()

#print y.input
#print y.activate()

#______________________________________________________



#Simple NOT
#______________________________________________________

#print "Neurons"
#x1 = Neuron([0])
#y = Neuron()

#print x1.axon
#print x1.addConnection(y, 1, 1)

#WITH DENDRITES
#layer1 = Dendrite([x1])
#layer2 = Dendrite([y])

#layer1.activate()
#layer1.communicate()
#layer2.activate()
#layer2.communicate()
#print layer2.setOutput()

#WITHOUT DENDRITES
#print x1.activate()
#print x1.communicate()

#print y.input
#print y.activate()

#______________________________________________________



#Network TESTS
#______________________________________________________
#net = Network()
#net = net.newRandom(2,3,1,3)
#print "show"
#net.show()
#net.clearIO()
#print net.activate([1])
#______________________________________________________


O \textit{script} contendo o seguinte código foi executado:\\\\
x1 = Neuron()	\#Neurônio de entrada\\
x2 = Neuron()	\#Neurônio de entrada\\
%
%Instância dos neurônios da camada de saída:\\
y1 = Neuron() 	\#Saída para \textit{AND}\\
y2 = Neuron()	\#Saída para \textit{OR}\\
%
%Conecta-se cada neurônio de uma camada a cada neurônio da próxima passando os parametros: neurônio a ser conectado; polarização da conexão; seu peso.\\
x1.addConnection(y1, 0, 0.5)	\#Conexão entre $x1$ e $y1$\\
x2.addConnection(y1, 0, 0.5)	\#Conexão entre $x2$ e $y1$\\
x1.addConnection(y2, 0, 0.6)	\#Conexão entre $x1$ e $y2$\\
x2.addConnection(y2, 0, 0.6)	\#Conexão entre $x2$ e $y2$\\
%
%Instâncias das camadas recebendo a lista de neurônios que as compõem:\\
layer1 = Dendrite([x1,x2])	\#Instância da camada de entrada\\
layer2 = Dendrite([y1,y2])	\#Instância da camada de saída\\
%
%Instancia da rede recebendo a lista de suas camadas ordenadas:\\
net = Network([layer1,layer2])	\#Instância da rede\\
%
%Limpam-se os valores de entradas e saídas dos componentes:\\
net.clearIO()	\#Limpeza dos valores de entradas e saídas dos componentes\\
%
%Ativa-se a rede imprimindo seus valores de retorno:\\
print net.activate([1,1])	\#Imprimir o retorno da ativação para a lista no escopo\\
print net.activate([0,1])	\#Imprimir o retorno da ativação para a lista no escopo\\
print net.activate([1,0])	\#Imprimir o retorno da ativação para a lista no escopo\\
print net.activate([0,0])	\#Imprimir o retorno da ativação para a lista no escopo\\
"""
