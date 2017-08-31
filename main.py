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

#recursive algorithm to generate a decision tree using ID3
def learn_tree(training_data,attributes):
	if not training_data:
		return None
	if is_pure(training_data):
		return new Node(classification = training_data[0].classification)
	if not attributes:
		majority = majority_count(training_data)
		return new Node(classification = majority)
	best_attribute = learn_attribute(training_data,attributes)
	left,right = split_data(best_attribute)
	attributes.remove(best_attribute)
	splitting_attribute = new Node(best_attribute)
	splitting_attribute.left = learn_tree(left,attributes)
	splitting_attribute.right = learn_tree(right,attributes)
	attributes.append(best_attribute)
	return splitting_attribute

#function to determine if all instances of data have the same classification, returns true if pure, else false
def is_pure(data):
	classification = data[0].classification
	for instance in data:
		if data.classification != classification:
			return False
	return True

#returns the majority classification 0 or 1 of a dataset
def majority_count(data):
	positive = 0
	for instance in data:
		if instance.classification == 1:
			positive +=1
	if positive / len(data) >= .5:
		return 1
	else:
		return 0

#algorithm for chosing attribute that will partition data with the lowest entropy
def learn_attribute(data,attributes):
	lowest_entropy = 2
	best_attribute = None
	for attr in attributes:
		conditional_entropy = conditional_entropy(data,attr)
		if conditional_entropy < lowest_entropy:
			lowest_entropy = conditional_entropy
			best_attribute = attr
	return best_attribute

#formula for calculating the conditional distribution entropy of a dataset when partitioned by a particular attribute
def conditional_entropy(data,attribute):
	total = len(data)
	left = [instance for instance in data if instance.attribute_dict[attribute] == 0]
	right = [instance for instance in data if instance.attribute_dict[attribute] == 1]
	left_entropy = entropy_calc(left)
	right_entropy = entropy_calc(right)
	return (len(left)/total) * (left_entropy) + (len(right)/total) * right_entropy


#takes a distribution and calculates entropy
def entropy_calc(data):
	positive,negative = 0,0
	for instance in data:
		if instance.classification == 0:
			negative +=1
		else:
			positive +=1
	negative_probability = negative/len(list)
	positive_probability = positive/len(list)
	if negative_probability == 0:
		left_entropy = 0
	else: 
		left_entropy = -1 * negative_probability * math.log(negative_probability,2)
	if positive_probability == 0:
		right_entropy = 0
	else:
		right_entropy = -1 * positive_probability * math.log(positive_probability,2)
	return left_entropy + right_entropy


training_data_list = List of training data objects
test_data_list = List of test data objects
attribute_list = List of valid attributes to split on

decision_tree = learn_tree(training_data_list,attribute_list)
print(decision_tree)
test(tree,training_data_list,test_data_list)