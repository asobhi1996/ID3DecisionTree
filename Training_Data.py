class Training_Data:
	def __init__(self,attributes,attr_values,classification):
		self.attr_dict = {attr : attr_value for attr,attr_value in zip(attributes,attr_values)}
		self.classification = classification

	def __repr__(self):
		return 'Attributes: {}\nClassification: {}\n'.format(self.attr_dict,self.classification)