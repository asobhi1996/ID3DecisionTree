"""
Main file for generating an ID3 tree from training data
Input: two command line arguments. First is a file with lableled training data and second is unlabeled test data. Training data includes up to N attributes and the last attribute must be the classification
All input files will be in the following format. The first line will contain a tab-seperated list of attribute names. The reamining lines correspond to a labeled data instance, and consist of a tab-seperated list of 0s or 1s, corresponding to each attribute.
Output: A decision tree object to classify data. The program will also outpout a visual representatino of the tree to the standard output and show training and test accuracy percentages.
"""

"""
Psudocode:
	read data and create two lists of data objects (list of Training_object and Test_Ojbect) and an attribute list
	recursively create the tree using ID3 algorithm as defined
	print the tree to standard output
	test the tree with the training and test data and report accuracies
"""

import math,sys
from Data import Data
from Node import Node

#recursive algorithm to generate a decision tree using ID3
def learn_tree(training_data,attributes):
	#base cases

	#there are no more data instances to classify
	if not training_data:
		return Node(classification = most_common_class)
	#this is a pure node, all data instances are of the same class
	if is_pure(training_data):
		return Node(classification = training_data[0].classification)
	#this is not a pure node, take the majority
	if not attributes:
		return Node(classification = majority_count(training_data))
	#otherwise, we are in the recusive case and must split the data by an attribute
	#proceed to find the attribute that will yield the highest information gain
	best_attribute = learn_attribute(training_data,attributes)
	left,right = split_data(training_data,best_attribute)
	attributes.remove(best_attribute)
	splitting_attribute_node = Node(attribute=best_attribute)
	splitting_attribute_node.left = learn_tree(left,attributes)
	splitting_attribute_node.right = learn_tree(right,attributes)
	attributes.append(best_attribute)
	return splitting_attribute_node

#split a list into 2 lists by attribute
def split_data(data,attr):
	left,right = [],[]
	for instance in data:
		left.append(instance) if instance.attr_dict[attr] == 0 else right.append(instance)
	return left,right 

#function to determine if all instances of data have the same classification, returns true if pure, else false
def is_pure(data):
	classification = data[0].classification
	for instance in data:
		if instance.classification != classification:
			return False
	return True

#returns the majority classification 0 or 1 of a dataset
def majority_count(data):
	positive_percent = len([True for instance in data if instance.classification == 1]) / float(len(data))
	if positive_percent == .5:
		return most_common_class
	else:
		return 1 if positive_percent > .5 else 0

#algorithm for chosing attribute that will partition data with the lowest entropy
def learn_attribute(data,attributes):
	lowest_entropy = 3
	best_attribute = None
	for attr in attributes:
		conditional_entropy = conditional_entropy_calc(data,attr)
		if conditional_entropy < lowest_entropy:
			lowest_entropy = conditional_entropy
			best_attribute = attr
		elif conditional_entropy == lowest_entropy:
			if attribute_order_list.index(attr) < attribute_order_list.index(best_attribute):
				best_attribute = attr
	return best_attribute

#formula for calculating the conditional distribution entropy of a dataset when partitioned by a particular attribute
def conditional_entropy_calc(data,attribute):
	total = float(len(data))
	left = [instance for instance in data if instance.attr_dict[attribute] == 0]
	right = [instance for instance in data if instance.attr_dict[attribute] == 1]
	left_entropy = entropy_calc(left)
	right_entropy = entropy_calc(right)
	return ((len(left)/total) * left_entropy) + ((len(right)/total) * right_entropy)


#takes a distribution and calculates entropy
def entropy_calc(data):
	if len(data) == 0:
		return 0
	negative = 0.0
	total = float(len(data))
	for instance in data:
		if instance.classification == 0:
			negative += 1
	negative_probability = negative/total
	positive_probability = (total-negative)/total
	if negative_probability == 0:
		left_entropy = 0
	else: 
		left_entropy = -1 * negative_probability * math.log(negative_probability,2)
	if positive_probability == 0:
		right_entropy = 0
	else:
		right_entropy = -1 * positive_probability * math.log(positive_probability,2)
	return left_entropy + right_entropy

#reads .dat file for training and test files, returns a list of attributes, list of training data objects, and list of test data objects
def read_data(filename,filename2):
	attributes_read = False
	training_data,test_data = [],[]
	with open(filename) as data_file:
			for line in data_file:
				if line.isspace():
					continue
				if not attributes_read:
					attribute_list = line.strip('\n').split('\t')
					#remove class "attribute" from attr list
					attribute_list = attribute_list[:-1]
					attributes_read = True
				else:
					val_lst = line.strip('\n').split('\t')
					training_data.append(Data(attribute_list,val_lst[:-1],val_lst[-1]))
	attributes_read = False
	with open(filename2) as data_file:
		for line in data_file:
			if line.isspace():
					continue
			if not attributes_read:
				attributes_read = True
			else:
				val_lst = line.strip('\n').split('\t')
				test_data.append(Data(attribute_list,val_lst[:-1],val_lst[-1]))
	return attribute_list,training_data,test_data

def print_decision_tree(decision_tree,depth):
	if decision_tree is None:
		print("ERROR")
		sys.exit()
	else:
		if decision_tree.attribute is not None:

			if decision_tree.left is not None:
				print("|  " * depth,end='')
				if decision_tree.left.attribute is not None:
					print('{} = 0 :'.format(decision_tree.attribute))
					print_decision_tree(decision_tree.left,depth+1)
				else:
					print('{} = 0 :\t{}'.format(decision_tree.attribute,decision_tree.left.classification))

			if decision_tree.right is not None:
				print("|  " * depth,end='')
				if decision_tree.right.attribute is not None:
					print('{} = 1 :'.format(decision_tree.attribute))
					print_decision_tree(decision_tree.right,depth+1)
				else:
					print('{} = 1 :\t{}'.format(decision_tree.attribute,decision_tree.right.classification))
		else:
			print(decision_tree.classification)

#function to test tree accuracy on a collection of data
def test_tree_accuracy(decision_tree,test_data):
	correct = 0.0
	for instance in test_data:
		if predicited_value(instance,decision_tree) == instance.classification:
			correct += 1
	return correct / len(test_data)

#given a tree and data, predicts the label of the data
def predicited_value(instance,tree):
	if tree.classification is not None:
		return tree.classification
	if instance.attr_dict[tree.attribute] == 0:
		return predicited_value(instance,tree.left)
	else:
		return predicited_value(instance,tree.right)

#main function
#reads data, learns the tree, tests accuracy, and prints to console
if __name__ == "__main__":
	attribute_list,training_data,test_data = read_data(sys.argv[1],sys.argv[2])
	most_common_class = majority_count(training_data + test_data)
	attribute_order_list = attribute_list.copy()
	decision_tree = learn_tree(training_data,attribute_list)
	print("Accuracy on training data ({} instances) is {:.2%}".format(len(training_data),test_tree_accuracy(decision_tree,training_data)))
	print("Accuracy on test data ({} instances) is {:.2%}".format(len(test_data),test_tree_accuracy(decision_tree,test_data)))
	print_decision_tree(decision_tree,0)