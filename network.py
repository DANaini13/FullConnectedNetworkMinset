import numpy as np
from loadImages import *

class Layer:
	def __init__(self, inputs_number, outputs_number):
		self.weights = np.random.rand(inputs_number+1, outputs_number) * 0.1 - 0.05
		self.last_diff = np.zeros(self.weights.shape)
		self.filter_func = lambda x: 1.0/(1 + np.exp(-x))
	
	def get_output(self, inputs):
		inputs = np.concatenate((inputs, np.array([1])), axis=0)
		self.inputs = inputs
		return [self.filter_func(i) for i in np.dot(inputs, self.weights)]
	
	def train(self, error, learning_rate, movement):
		weights_diff = []
		for single_error in error:
			weights_diff.append(learning_rate * single_error * self.inputs)
		self.weights += np.array(weights_diff).T + self.last_diff * movement
		self.last_diff = np.array(weights_diff).T

	def get_input_error(self, error):
		input_error = []
		for single_weights in self.weights:
			input_error.append(np.dot(error, single_weights))
		input_error = np.array(input_error)
		return self.inputs * (1 - self.inputs) * input_error


class Network:
	"""
	hidden_layers: a list that store the number of hidden units in each layer.
					example: [20] gonna create one hidden layer with 20 units,
							 [20, 50] gonna create two hidden layer with 20
							 and 50 units.
	input_nums: the lengh of each input as a list or one D numpy array
	outputs_nums: the number of units in the output layer.
	"""
	def __init__(self, hidden_layers, input_nums, outputs_nums):
		self.hidden_layers = []
		for x in range(len(hidden_layers) - 1):
			self.hidden_layers.append(Layer(hidden_layers[x], hidden_layers[x + 1])) 
		if len(hidden_layers) > 0:
			self.hidden_layers.append(Layer(hidden_layers[len(hidden_layers)-1], outputs_nums))
			self.input_layer = Layer(input_nums, hidden_layers[0])
		else:
			self.input_layer = Layer(input_nums, outputs_nums)

	"""
	this function gonna generate outputs for a specific input
	"""
	def get_output(self, inputs):
		if len(self.hidden_layers) <= 0:
			self.output = self.input_layer.get_output(inputs)
			return self.output
		else:
			self.output = self.input_layer.get_output(inputs)
			for layer in self.hidden_layers:
				self.output = layer.get_output(self.output)
			return self.output

	"""
	calling this function when the output result is not correct.
	"""
	def train(self, learning_rate, movement, filter_func, target):
		filtered_out = np.array([filter_func(i) for i in self.output])
		error = self.output * (1 - filtered_out) * (target - self.output)
		if len(self.hidden_layers) <= 0:
			self.input_layer.train(error, learning_rate, movement)
		else:
			hidden_num = len(self.hidden_layers)
			self.hidden_layers[hidden_num - 1].train(error, learning_rate, movement)
			input_error = self.hidden_layers[hidden_num - 1].get_input_error(error)
			for x in range(hidden_num - 1):
				index = hidden_num -x -2
				self.hidden_layers[index].train(input_error[:-1], learning_rate, movement)
				input_error = self.hidden_layers[index].get_input_error(input_error[:-1])
			self.input_layer.train(input_error[:-1], learning_rate, movement)

class Controller:
	"""
	network: the neural network which created by Network class.
	write a new Controller class if you wanna define a new training process.
	"""
	def __init__(self, network, train_inputs, train_labels, test_inputs, test_labels):
		self.network = network
		self.train_inputs = train_inputs
		self.train_labels = train_labels
		self.test_inputs = test_inputs
		self.test_labels = test_labels
		self.filter_func = lambda x: 1.0/(1 + np.exp(-x))

	def start(self):
		for x in range(50):
			total = 0
			correct = 0
			inputCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			for input, label, in zip(self.train_inputs, self.train_labels):
				inputCount[label] += 1
				if inputCount[label] % 2 != 0:
					continue
				output = network.get_output(np.array(input))
				result = np.argmax(output)
				if(result == label):
					correct += 1
				else:
					target = np.full((10), 0.1)
					target[label] = 0.9
					network.train(0.1, 0.9, self.filter_func, target)
				total += 1
			test_total = 0
			test_correct = 0
			for input, label, in zip(self.test_inputs, self.test_labels):
				output = network.get_output(np.array(input))
				result = np.argmax(output)
				if(result == label):
					test_correct += 1
				test_total += 1
				if x >= 49:
					print("3-" + str(result) + "-" + str(label)) #this output gonna be read by the excel generator 
					#3- means the final outputs and targets to generate the confustion matrix

			print("1-" + str(correct/total))  #this output gonna be read by the excel generator 
			#1- means training accuracy
			print("2-" + str(test_correct/test_total))  #this output gonna be read by the excel generator 
			#2- means testing accuracy



############################### Program start here ###############################
trainingData = list(read(dataset='training', path='./DataSet'))
temp = trainingData
labels = [i[0] for i in temp]
pixels = [i[1] for i in temp]
pixels = np.array(pixels)
pixels = pixels.reshape((60000, 784))
pixels = pixels/255

testingData = list(read(dataset='testing', path='./DataSet'))
temp = testingData
test_labels = [i[0] for i in temp]
test_pixels = [i[1] for i in temp]
test_pixels = np.array(test_pixels)
test_pixels = test_pixels.reshape((10000, 784))
test_pixels = test_pixels/255


network = Network([100], 784, 10)
controller = Controller(network, pixels, labels, test_pixels, test_labels)
controller.start()

