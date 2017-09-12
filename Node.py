#Tree Node class for the decision tree
#left indicates 0, right indicates 1
#if attributes is none, then it is an leaf node, otherwise, classification is none and it is an internal node
class Node:
	def __init__(self,attribute=None,classification=None):
		self.attribute = attribute
		self.left = None
		self.right = None
		self.classification = classification

	def is_leaf(self):
		if self.attribute is None and self.classification is not None:
			return True
		else:
			return False