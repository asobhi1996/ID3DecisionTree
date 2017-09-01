class Data:
	def __init__(self,attributes,attr_values,classification):
		self.attr_dict = {attr : int(attr_value) for attr,attr_value in zip(attributes,attr_values)}
		self.classification = int(classification)

	def __repr__(self):
		return 'Atr: {}.Class: {}\n'.format(self.attr_dict,self.classification)