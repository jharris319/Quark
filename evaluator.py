from recognizer import *
from environment import *
from types import *


class Evaluator:

	def __init__(self, filename):
		self.environment = create()
		recognizer = Recognizer(filename)
		self.tree = recognizer.program()

	def eval(self, tree, env):
		f = self.get_eval_function(tree.type_)
		if f is None:
			raise Exception("no evaluation function for type " + tree.type_)
		else:
			return f(tree, env)

	def get_eval_function(self, type_):
		print(type_)
		if type_ is "program":
			return self.eval_program
		elif type_ is "var_def":
			return self.eval_var_def
		elif type_ is STRING:
			return self.eval_string
		elif type_ is INTEGER:
			return self.eval_integer
		elif type_ is REAL:
			return self.eval_real
		elif type_ is PLUS:
			return self.eval_plus
		elif type_ is MINUS:
			return self.eval_minus
		elif type_ is MULTIPLY:
			return self.eval_multiply
		elif type_ is DIVIDE:
			return self.eval_divide
		elif type_ is EXPONENT:
			return self.eval_exponent
		elif type_ is MODULUS:
			return self.eval_modulus
		elif type_ is IF:
			return self.eval_if
		elif type_ is "opt_elif":
			return self.eval_opt_elif
		elif type_ is "opt_else":
			return self.eval_opt_else
		elif type_ is LT:
			return self.eval_lt
		elif type_ is GT:
			return self.eval_gt
		elif type_ is LTE:
			return self.eval_lte
		elif type_ is GTE:
			return self.eval_gte
		elif type_ is NOTEQUAL:
			return self.eval_notequal
		elif type_ is EQUALITY:
			return self.eval_equality
		elif type_ is "block":
			return self.eval_block
		elif type_ is PRINT:
			return self.eval_print
		else:
			print("\nOops, I haven't implemented:", type_, "\n\n")

	def eval_program(self, tree, env):
		self.eval(tree.left, env)
		if tree.right is not None:
			return self.eval(tree.right, env)
		else:
			print("Hooray! I'm done.")

	def eval_var_def(self, tree, env):
		# print("VAR:", tree.left.value, "is", self.eval(tree.right, env).value)
		insert(tree.left.value, self.eval(tree.right, env), env)

	def eval_string(self, tree, env):
		return tree

	def eval_integer(self, tree, env):
		return tree

	def eval_real(self, tree, env):
		return tree

	def eval_plus(self, tree, env):
		val = self.eval(tree.left, env).value + self.eval(tree.right, env).value
		if type(val) is int:
			return Lexeme(INTEGER, val)
		else:
			return Lexeme(REAL, val)

	def eval_minus(self, tree, env):
		val = self.eval(tree.left, env).value - self.eval(tree.right, env).value
		if type(val) is int:
			return Lexeme(INTEGER, val)
		else:
			return Lexeme(REAL, val)

	def eval_multiply(self, tree, env):
		val = self.eval(tree.left, env).value * self.eval(tree.right, env).value
		if type(val) is int:
			return Lexeme(INTEGER, val)
		else:
			return Lexeme(REAL, val)

	def eval_divide(self, tree, env):
		val = self.eval(tree.left, env).value / self.eval(tree.right, env).value
		if type(val) is int:
			return Lexeme(INTEGER, val)
		else:
			return Lexeme(REAL, val)

	def eval_exponent(self, tree, env):
		val = self.eval(tree.left, env).value ** self.eval(tree.right, env).value
		if type(val) is int:
			return Lexeme(INTEGER, val)
		else:
			return Lexeme(REAL, val)

	def eval_modulus(self, tree, env):
		val = self.eval(tree.left, env).value % self.eval(tree.right, env).value
		if type(val) is int:
			return Lexeme(INTEGER, val)
		else:
			return Lexeme(REAL, val)

	def eval_if(self, tree, env):
		glue = tree.left
		opt_elif = tree.right
		condition = self.eval(glue.left, env)
		if condition.type_ is BOOLTRUE:
			print("WINNER! -- IF")
			# return self.eval(glue.right, env)
		condition = self.eval(opt_elif, env)
		if condition.type_ is BOOLTRUE:
			return print("WINNER! -- ELIF")
		opt_else = opt_elif.right
		while opt_else.right is not None:
			opt_else = opt_else.right
		self.eval(opt_else, env)

	def eval_opt_elif(self, tree, env):
		glue = tree.left
		condition = self.eval(glue.left, env)
		if condition.type_ is BOOLTRUE:
			# self.eval(glue.right, env)
			pass
		else:
			if tree.right.type_ is "opt_elif":
				condition = self.eval(tree.right, env)
		return condition

	def eval_opt_else(self, tree, env):
		glue = tree.left
		print("WINNER! -- ELSE")
		return self.eval(glue.left, env)

	def eval_lt(self, tree, env):
		boolVal = self.eval(tree.left, env).value < self.eval(tree.right, env).value
		print(boolVal)
		if boolVal is True:
			return Lexeme(BOOLTRUE)
		else:
			return Lexeme(BOOLFALSE)

	def eval_gt(self, tree, env):
		boolVal = self.eval(tree.left, env).value > self.eval(tree.right, env).value
		print(boolVal)
		if boolVal is True:
			return Lexeme(BOOLTRUE)
		else:
			return Lexeme(BOOLFALSE)

	def eval_lte(self, tree, env):
		boolVal = self.eval(tree.left, env).value <= self.eval(tree.right, env).value
		print(boolVal)
		if boolVal is True:
			return Lexeme(BOOLTRUE)
		else:
			return Lexeme(BOOLFALSE)

	def eval_gte(self, tree, env):
		boolVal = self.eval(tree.left, env).value >= self.eval(tree.right, env).value
		print(boolVal)
		if boolVal is True:
			return Lexeme(BOOLTRUE)
		else:
			return Lexeme(BOOLFALSE)

	def eval_notequal(self, tree, env):
		boolVal = self.eval(tree.left, env).value != self.eval(tree.right, env).value
		print(boolVal)
		if boolVal is True:
			return Lexeme(BOOLTRUE)
		else:
			return Lexeme(BOOLFALSE)

	def eval_equality(self, tree, env):
		boolVal = self.eval(tree.left, env).value == self.eval(tree.right, env).value
		print(boolVal)
		if boolVal is True:
			return Lexeme(BOOLTRUE)
		else:
			return Lexeme(BOOLFALSE)

	def eval_block(self, tree, env):
		self.eval(tree.left, env)
		if tree.right is not None:
			return self.eval(tree.left.right, env)

	def eval_print(self, tree, env):
		value = self.eval(tree.left, env)
		print(value.value)

	def eval_while(self, tree, env):
		pass
