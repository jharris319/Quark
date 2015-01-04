class Lexeme:

	def __init__(self, type_=None, value=None):
		self.type_ = type_
		self.value = value
		self.left = None
		self.right = None