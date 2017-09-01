"""
Main file for generating an ID3 tree from training data
Input: two command line arguments. First is a file with lableled training data and second is unlabeled test data. Training data includes up to N attributes and the last attribute must be the classification
Output: A decision tree object to classify data. The program will also outpout a visual representatino of the tree to the standard output and show training and test accuracy percentages.
"""

"""
Psudocode:
	read data and create two lists of data objects (list of Training_object and Test_Ojbect) and an attribute list
	recursively create the tree using ID3 algorithm as defined
	print the tree to standard output
	test the tree with the training and test data and report accuracies
"""

import math
from Data import Data
from Node import Node

#recursive algorithm to generate a decision tree using ID3
def learn_tree(training_data,attributes):
	if not training_data:
		return None
	if is_pure(training_data):
		return Node(classification = training_data[0].classification)
	if not attributes:
		return Node(classification = majority_count(training_data))
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
	return 1 if (len([True for instance in data if instance.classification == 1]) / float(len(data)) >= .5) else 0

#algorithm for chosing attribute that will partition data with the lowest entropy
def learn_attribute(data,attributes):
	lowest_entropy = 3
	best_attribute = None
	for attr in attributes:
		conditional_entropy = conditional_entropy_calc(data,attr)
		if conditional_entropy < lowest_entropy:
			lowest_entropy = conditional_entropy
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
				if not attributes_read:
					attribute_list = line.rstrip('\n').split('\t')
					attribute_list = attribute_list[:-1]
					attributes_read = True
				else:
					val_lst = line.rstrip('\n').split('\t')
					training_data.append(Data(attribute_list,val_lst[:-1],val_lst[-1]))
	attributes_read = False
	with open(filename2) as data_file:
		for line in data_file:
			if not attributes_read:
				attributes_read = True
			else:
				val_lst = line.rstrip('\n').split('\t')
				test_data.append(Data(attribute_list,val_lst[:-1],val_lst[-1]))
	return attribute_list,training_data,test_data

def print_decision_tree(decision_tree):
	if decision_tree is None:
		pass
	else:
		if decision_tree.attribute is not None:
			if decision_tree.left is not None:
				print('{} = 0 :|'.format(decision_tree.attribute))
				print_decision_tree(decision_tree.left)
			if decision_tree.right is not None:
				print('{} = 1: |'.format(decision_tree.attribute))
				print_decision_tree(decision_tree.right)
		else:
			print('{}'.format(decision_tree.classification))

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

attribute_list,training_data,test_data = read_data('train.dat','test.dat')
decision_tree = learn_tree(training_data,attribute_list)
print(test_tree_accuracy(decision_tree,training_data))
print(test_tree_accuracy(decision_tree,test_data))
