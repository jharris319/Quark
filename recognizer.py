from lexer import *


class Recognizer:

	def __init__(self, filename):
		self.i = Lexer(filename)
		self.currentLexeme = self.i.lex()

	### Support functions
	def advance(self):
		self.currentLexeme = self.i.lex()
		# print("on line:", self.i.line_number)
		# print(self.currentLexeme.type_, self.currentLexeme.value)

	def check(self, type_):
		# if self.currentLexeme.type_ == type_:
		# 	print(type_)
		return self.currentLexeme.type_ == type_

	def match(self, type_):
		# print("match:", type_)
		self.match_no_advance(type_)
		pending_return = self.currentLexeme
		self.advance()
		return pending_return

	def match_no_advance(self, type_):
		if not self.check(type_):
			print("bad:", type_)
			print("Syntax error on line ", self.i.line_number, "\nUnexpected ", self.currentLexeme.type_, sep='')
			exit(1)
		#else:
			#print("good:", type_, "\n val:", self.currentLexeme.value, "\n line:", self.i.line_number, "\n")

	### Parsing functions
	def array(self):
		tree = Lexeme("array")
		self.match(ARRAY)
		self.match(OBRACKET)
		tree.left = self.opt_integer()
		self.match(CBRACKET)
		return tree

	def block(self):		# TODO: Definitions
		tree = Lexeme("block")
		if self.var_definition_pending():
			tree.left = self.var_definition()
			tree.right = self.block()
		elif self.statement_list_pending():
			tree.left = self.statement_list()
		else:
			tree.left = Lexeme("epsilon")
		return tree

	def class_block(self):
		tree = self.program()
		return tree

	def class_definition(self):
		tree = Lexeme("class_def")
		self.match(CLASS)
		tree.left = self.match(ID)
		tree.right = self.class_block()
		self.match(END)
		return tree

	def definition(self):
		tree = Lexeme("definition")
		if self.var_definition_pending():
			tree = self.var_definition()
		elif self.func_definition_pending():
			tree = self.func_definition()
		elif self.class_definition_pending():
			tree = self.class_definition()
		return tree

	def expression(self):
		if self.number_pending():
			tmp = self.number()
			if self.operator_pending():
				tree = self.operator()
				tree.left = tmp
				tree.right = self.expression()
			else:
				tree = tmp
		elif self.check(ID):
			tmp = self.match(ID)
			if self.operator_pending():
				tree = self.operator()
				tree.left = tmp
				tree.right = self.expression()
			elif self.check(OBRACKET):		# Array
				tree = Lexeme("array")
				tree.left = tmp
				self.match(OBRACKET)
				tree.right = self.expression()
				self.match(CBRACKET)
				tree.right.left = self.match(ASSIGN)
				tree.right.left.left = self.primary()
			elif self.check(OPAREN):		# Function Calls
				tree = Lexeme("func_call")
				tree.left = tmp
				self.match(OPAREN)
				tree.right = self.opt_param_list()
				self.match(CPAREN)
			else:
				tree = tmp
		elif self.check(OPAREN):
			self.match(OPAREN)
			tree = self.expression()
			self.match(CPAREN)
		else:
			tree = self.logic_primary()
		return tree

	def func_definition(self):
		tree = Lexeme("func_def")
		self.match(DEF)
		tree.left = self.match(ID)
		self.match(OPAREN)
		tree.right = self.opt_param_list()
		node = tree.right
		while(node.right is not None):
			node = node.right
		self.match(CPAREN)
		node.right = self.block()
		self.match(END)
		return tree

	def if_statement(self):
		tree = Lexeme("if")
		self.match(IF)
		self.match(OPAREN)
		glue = Lexeme("glue")
		tree.left = glue
		glue.left = self.logic_expr()
		self.match(CPAREN)
		self.match(THEN)
		glue.right = self.block()
		tree.right = self.opt_elif()
		node = tree.right
		while(node.right is not None):
			node = node.right
		node.right = self.opt_else()
		self.match(FI)
		return tree

	def logic_expr(self):
		if self.primary_pending():
			tmp = self.primary()
			if self.logic_operator_pending():
				tree = self.logic_operator()
				tree.left = tmp
				tree.right = self.logic_expr()
			else:
				tree = tmp
		elif self.logic_primary_pending():
			tmp = self.logic_primary()
			if self.logic_operator_pending():
				tree = self.logic_operator()
				tree.left = tmp
				tree.right = self.logic_expr()
			else:
				tree = tmp
		else:
			tree = self.logic_operator()
			tree.right = self.logic_primary()
		return tree

	def logic_primary(self):
		if self.check(BOOLTRUE):
			tree = self.match(BOOLTRUE)
		elif self.check(BOOLFALSE):
			tree = self.match(BOOLFALSE)
		else:
			tree = self.match(ID)
		return tree

	def logic_operator(self):
		if self.check(LT):
			tree = self.match(LT)
		elif self.check(LTE):
			tree = self.match(LTE)
		elif self.check(GT):
			tree = self.match(GT)
		elif self.check(GTE):
			tree = self.match(GTE)
		elif self.check(EQUALITY):
			tree = self.match(EQUALITY)
		elif self.check(NOTEQUAL):
			tree = self.match(NOTEQUAL)
		elif self.check(AND):
			tree = self.match(AND)
		elif self.check(OR):
			tree = self.match(OR)
		else:
			tree = self.match(NOT)
		return tree

	def number(self):
		if self.check(INTEGER):
			tree = self.match(INTEGER)
		else:
			tree = self.match(REAL)
		return tree

	def operator(self):
		if self.check(PLUS):
			tree = self.match(PLUS)
		elif self.check(MINUS):
			tree = self.match(MINUS)
		elif self.check(MULTIPLY):
			tree = self.match(MULTIPLY)
		elif self.check(DIVIDE):
			tree = self.match(DIVIDE)
		elif self.check(MODULUS):
			tree = self.match(MODULUS)
		elif self.check(ASSIGN):
			tree = self.match(ASSIGN)
		else:
			tree = self.match(EXPONENT)
		return tree

	def opt_elif(self):
		tree = Lexeme("opt_elif")
		if self.check(ELIF):
			self.match(ELIF)
			self.match(OPAREN)
			glue = Lexeme("glue")
			tree.left = glue
			glue.left = self.logic_expr()
			self.match(CPAREN)
			self.match(THEN)
			glue.right = self.block()
			if self.check(ELIF):
				tree.right = self.opt_elif()
		else:
			tree.left = Lexeme("epsilon")
		return tree

	def opt_else(self):
		tree = Lexeme("opt_else")
		if self.check(ELSE):
			self.match(ELSE)
			tree.left = self.block()
		else:
			tree.left = Lexeme("epsilon")
		return tree

	def opt_integer(self):
		if self.check(INTEGER):
			tree = self.match(INTEGER)
		else:
			tree = Lexeme("epsilon")
		return tree

	def opt_param_list(self):
		if self.param_list_pending():
			tree = self.param_list()
		else:
			tree = Lexeme("epsilon")
		return tree

	def param_list(self):
		tree = Lexeme("param_list")
		if self.primary_pending():
			tree.left = self.primary()
			if self.check(COMMA):
				self.match(COMMA)
				tree.right = self.param_list()
		return tree

	def primary(self):
		if self.check(INTEGER):
			tree = self.match(INTEGER)
		elif self.check(REAL):
			tree = self.match(REAL)
		elif self.check(STRING):
			tree = self.match(STRING)
		else:
			tree = self.match(ID)
		return tree

	def print_statement(self):
		tree = Lexeme("print")
		self.match(PRINT)
		self.match(OPAREN)
		tree.left = self.primary()
		self.match(CPAREN)
		return tree

	def program(self):
		tree = Lexeme("program")
		if self.definition_pending():
			tree.left = self.definition()
			if self.program_pending():
				tree.right = self.program()
		else:
			tree.left = self.statement()
			if self.program_pending():
				tree.right = self.program()
		return tree

	def return_statement(self):
		tree = Lexeme("return")
		self.match(RETURN)
		tree.left = self.expression()
		return tree

	def statement(self):
		if self.expression_pending():
			tree = self.expression()
		elif self.if_statement_pending():
			tree = self.if_statement()
		elif self.while_statement_pending():
			tree = self.while_statement()
		elif self.return_statement_pending():
			tree = self.return_statement()
		else:
			tree = self.print_statement()
		return tree

	def statement_list(self):
		tree = Lexeme("statement_list")
		tree.left = self.statement()
		if self.statement_list_pending():
			tree.right = self.statement_list()
		return tree

	def var_definition(self):
		tree = Lexeme("var_def")
		self.match(VAR)
		tree.left = self.match(ID)
		self.match(ASSIGN)
		if self.expression_pending():
			tree.right = self.expression()
		elif self.primary_pending():
			tree.right = self.primary()
		elif self.array_pending():
			tree.right = self.array()
		else:
			tree.right = self.logic_expr()
		return tree

	def while_statement(self):
		tree = Lexeme("while")
		self.match(WHILE)
		self.match(OPAREN)
		tree.left = self.logic_expr()
		self.match(CPAREN)
		self.match(DO)
		tree.right = self.block()
		self.match(END)
		return tree


	### Pending functions
	def array_pending(self):
		return self.check(ARRAY)

	def class_block_pending(self):
		return self.var_definition_pending() | self.func_definition_pending() | self.func_definition_pending()

	def class_definition_pending(self):
		return self.check(CLASS)

	def definition_pending(self):
		return self.var_definition_pending() | self.func_definition_pending() | self.class_definition_pending()

	def expression_pending(self):
		return self.number_pending() | self.check(ID) | self.check(OPAREN)

	def func_definition_pending(self):
		return self.check(DEF)

	def if_statement_pending(self):
		return self.check(IF)

	def logic_operator_pending(self):
		return self.check(LT) | self.check(LTE) | self.check(GT) | self.check(GTE)\
			| self.check(EQUALITY) | self.check(AND) | self.check(OR) | self.check(NOT) | self.check(NOTEQUAL)

	def logic_primary_pending(self):
		return self.check(BOOLTRUE) | self.check(BOOLFALSE) | self.check(ID)

	def number_pending(self):
		return self.check(INTEGER) | self.check(REAL)

	def operator_pending(self):
		return self.check(PLUS) | self.check(MINUS) | self.check(MULTIPLY)\
			| self.check(DIVIDE) | self.check(MODULUS) | self.check(EXPONENT)\
			| self.check(ASSIGN)

	def param_list_pending(self):
		return self.primary_pending()

	def primary_pending(self):
		return self.check(INTEGER) | self.check(REAL) | self.check(STRING) | self.check(ID)

	def program_pending(self):
		return self.definition_pending() | self.statement_pending()

	def return_statement_pending(self):
		return self.check(RETURN)

	def statement_pending(self):
		return self.expression_pending() | self.if_statement_pending()\
			| self.while_statement_pending() \
			| self.return_statement_pending() | self.check(PRINT)

	def statement_list_pending(self):
		return self.statement_pending()

	def var_definition_pending(self):
		return self.check(VAR)

	def while_statement_pending(self):
		return self.check(WHILE)