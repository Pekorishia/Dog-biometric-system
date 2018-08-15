import csv
import math
import random
import pprint
import operator 
from os import listdir				
from os.path import isfile, join	

# Force the results to be repeatable
# random.seed(1000)

# retrieves k random instances from the class data
def ReservoirSampling(dataSet, split, trainingSet=[] , testSet=[]):
	
	# calculates the number of training samples needed
	k = len(dataSet)*split

	for x in range(len(dataSet)):
		# if this is one of the k first instance seen
		if ( x < k):
			# add the instance into the training set
			trainingSet.append(dataSet[x])
		else:
			# randomly choose an integer that is between 0 and x (inclusive)
			# this will decrease the probability of replacing elements 
			# after every loop
			r = random.randint(0, x)

			# if r is in the range of the training set
			if (r < k):
				# add the soon to be removed instance into the test set
				testSet.append(trainingSet[r])
				# add the new instance into the training set
				trainingSet[r] = dataSet[x]
			else:
				# add the new instance into the test set
				testSet.append(dataSet[x])


# load all instances data and split them in training and test lists
def loadAllData(filesDir, allInstances, trainingSet, testSet, split, classList):
	# get all class filename
	filesList = [f for f in listdir(filesDir) if isfile(join(filesDir, f))]

	# for every file
	for file in filesList:
		# load it
		dataSet = loadData(filesDir+file)
		# split its instances into training and test ones
		ReservoirSampling(dataSet, split, trainingSet, testSet)
		# put the loaded data into the instance list
		allInstances.extend(dataSet)
		# put the dataSet class into the class list
		classList.append(dataSet[0][-1])


# opens the data file and returns the normalized dataset 
def loadData(filename):
	# open the data file
	with open(filename, 'rs') as csvfile:
		# get all the file lines
	    lines = csv.reader(csvfile, delimiter=' ', quotechar='|')
	    dataset = list(lines)

	    # loop into all lines
	    for x in range(len(dataset)):
	    	# split the string in the ','
	    	breaker = dataset[x][0].split(',')

	    	# for each float element, convert it to float
	    	for y in range(len(breaker)-1):
	    		breaker[y] = float(breaker[y])

	    	# put the split data into the dataset
	    	dataset[x] = breaker

	return dataset


# returns a string representation of the list
def string(text):
	return ",".join(str(y) for y in text)


# initializes the incorrect guess count dictionary 
def initializeGuess(dataSet):
	# create an vector with the same size as the data set
	strTest = [0] * len(dataSet)

	# for each training instances
	for x in range(len(strTest)):
		# put its string convertion into strTest
		strTest[x] = string(dataSet[x])


	# creates a dictionary with the keys being the instances 
	# as string and the values 0
	incorrectGuess = {key: 0 for key in strTest}

	return incorrectGuess
	    	

# calculates the euclidean distance between two instances
# based on the parameters that ranges from 0 to length
def euclideanDistance(instance1, instance2, length):
	distance = 0

	# calculates the sum(x1 - x2)^2 from x = 0 to x = length
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)

	return math.sqrt(distance)


# get the k nearest training set instances based on the
# test instance
def getNeighbors(trainingSet, testInstance, k):
	distances = []
	neighbors = []

	length = len(testInstance)-1

	# for all training instances
	for x in range(len(trainingSet)):
		# calculate the distance between them and the test one
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		# put the current training instance and its distance into a tuple record
		distances.append((trainingSet[x], dist))

	# sorts the tuples by the distance, which is the value
	# that operator.itemgetter(1) will get. 
	distances.sort(key=operator.itemgetter(1))

	# put the first k tuples inside the neighbors array
	for x in range(k):
		neighbors.append(distances[x][0])

	return neighbors


# returns the class that the majority of the neighbors
# belongs to
# In the case of a draw, the first one will be returned
def getResponse(neighbors):
	# an empty DICTIONARY
	classVotes = {}

	# for all neighbors
	for x in range(len(neighbors)):
		# get the last cell that has the class label
		response = neighbors[x][-1]

		# if it already exists in classVotes, then 
		# put one vote into it.
		if response in classVotes:
			classVotes[response] += 1
		else:
			# just initialize with 1 vote
			classVotes[response] = 1

	# sort the classVotes dictionary by the number of votes
	# in a decreasing order
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)

	return sortedVotes[0][0]


# calculates the accuracy of the algorithm
def getAccuracy(testSet, predictions):
	correct = 0
	# for every test instance
	for x in range(len(testSet)):
		# if the prediction was correct
		if testSet[x][-1] == predictions[x]:
			correct += 1
	# return the percentage of the correct/tests		
	return (correct/float(len(testSet))) * 100.0


# generates an empty confusion matrix based on the class list
def generateConfusionMatrix(classList, confusionMatrix, loopTimes):
	# from 0 to loopTimes-1
	for loop in range(loopTimes):
		aux = {}
		# for every element in class list
		for i in range (len(classList)):
			aux2 = {}
			# populates the aux dictionary with all classes as key 
			for j in range(len(classList)):
				aux2[classList[j]] = 0

			# populates the aux dictionary with the aux2
			# to make an matrix classXclass
			aux[classList[i]] = aux2 
		# populates the confusionmatrix dictionary with aux
		# to make it loopTimesXclassXclass
		confusionMatrix[loop] = aux

	return confusionMatrix


def knnAlgorithm(trainingSet, testSet, k, confusionMatrix, predictions, incorrectGuess):
	# generate predictions	
	for x in range(len(testSet)):
		# generate the k nearest neighbors 
		neighbors = getNeighbors(trainingSet, testSet[x], k)
		# get the classification class
		result = getResponse(neighbors)
		# put the predicted class into the predictions list
		predictions.append(result)
		
		# put the prediction and actual class in the confusionMatrix list
		confusionMatrix[testSet[x][-1]][result] += 1

		# if the classification was wrong
		if result != testSet[x][-1]:
			# for all neighbors
			for neighbor in neighbors:
				# which is from a different class
				if (testSet[x][-1] != neighbor[-1]):
					# add the error count of the instance
					incorrectGuess[string(neighbor)] = incorrectGuess[string(neighbor)] + 1
	
	# calculate the accuracy of the algorithm
	accuracy = getAccuracy(testSet, predictions)

	return accuracy


# prints the incorrectGuess dictionary and average accuracy into a output file
def printToFile(incorrectOutput, incorrectGuess, averageAcc):
	# open a .txt file
	file = open(incorrectOutput, "w")

	# for each element in incorrectGuess
	for inst in incorrectGuess:
		# print the dictionary
		file.write(inst + ':	' + str(incorrectGuess[inst]) + '\n')

	# print the average accuracy
	file.write('\naverage: ' + str(averageAcc))

	# close the .txt file
	file.close() 


def main():
	# initiate all data needed
	confusionMatrix = {}
	incorrectGuess = []
	allInstances=[]
	predictions=[]
	trainingSet=[]
	classList=[]
	testSet=[]

	# setup the split to 67:33 and k to 1
	split = 0.67
	k = 1

	# setup the number of times the algorithm will loop and the average accuracy
	loopTimes = 1
	averageAcc = 0

	# load all instances data and split them in training and test lists
	loadAllData('vectors/', allInstances, trainingSet, testSet, split, classList)
	
	# generate the dictionary with all instances and its error count as 0
	incorrectGuess = initializeGuess(allInstances)

	# generate the empty confusion matrix
	confusionMatrix = generateConfusionMatrix(classList, confusionMatrix, loopTimes)

	# for every loop
	for loop in range(loopTimes):
		averageAcc = averageAcc + knnAlgorithm(trainingSet, testSet, k, confusionMatrix[loop], predictions, incorrectGuess)

	# calculate the average
	averageAcc = averageAcc / loopTimes;
	
	# print average and incorrectGuess to output file
	printToFile('incorrectOutput.txt', incorrectGuess, averageAcc)

# call the main
main()