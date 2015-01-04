from lexeme import *
from types import *


class Lexer:

	def __init__(self, filename):
		self.file = open(filename, "r")
		self.line_number = 1

	def lex(self):
		self._skip_whitespace()
		pos = self.file.tell()
		ch = self.file.read(1)

		if ch is '(':
			return Lexeme(OPAREN, ch)
		elif ch is ')':
			return Lexeme(CPAREN, ch)
		elif ch is ',':
			return Lexeme(COMMA, ch)
		elif ch is '+':
			return Lexeme(PLUS, ch)
		elif ch is '*':
			return Lexeme(MULTIPLY, ch)
		elif ch is '-':
			nextCh = self.file.read(1)
			if nextCh.isdigit():
				self.file.seek(self.file.tell() - 2)
				return self._lex_digit()
			else:
				self.file.seek(self.file.tell() - 1)
				return Lexeme(MINUS, ch)
		elif ch is ':':
			return Lexeme(COLON, ch)
		elif ch is '/':
			return Lexeme(DIVIDE, ch)
		elif ch is '%':
			return Lexeme(MODULUS, ch)
		elif ch is '&':
			return Lexeme(AND, ch)
		elif ch is '$':
			return Lexeme(VAR, ch)
		elif ch is '|':
			return Lexeme(OR, ch)
		elif ch is '[':
			return Lexeme(OBRACKET, ch)
		elif ch is ']':
			return Lexeme(CBRACKET, ch)
		elif ch is '^':
			return Lexeme(EXPONENT, ch)
		elif ch is '<':
			nextCh = self.file.read(1)
			if nextCh is '=':
				return Lexeme(LTE, '<=')
			else:
				self.file.seek(self.file.tell() - 1)
				return Lexeme(LT, ch)
		elif ch is '>':
			nextCh = self.file.read(1)
			if nextCh is '=':
				return Lexeme(GTE, '>=')
			else:
				self.file.seek(self.file.tell() - 1)
				return Lexeme(GT, ch)
		elif ch is '!':
			nextCh = self.file.read(1)
			if nextCh is '=':
				return Lexeme(NOTEQUAL, '!=')
			else:
				self.file.seek(self.file.tell() - 1)
				return Lexeme(NOT, '!')
		elif ch is '=':
			nextCh = self.file.read(1)
			if nextCh is '=':
				return Lexeme(EQUALITY, '==')
			else:
				self.file.seek(self.file.tell() - 1)
				return Lexeme(ASSIGN, ch)
		elif ch is ';':
			return Lexeme(SEMICOLON, ch)
		elif ch is '':
			return Lexeme(EOF, 'EOF')
		else:
			if ch.isdigit() or ch is '.' or ch is '-':
				self.file.seek(pos)
				return self._lex_digit()
			elif ch.isalpha():
				self.file.seek(pos)
				return self._lex_identifier()
			elif ch is '\"':
				self.file.seek(pos)
				return self._lex_string()
			else:
				return Lexeme("UNKNOWN", ch)

	def _skip_whitespace(self):
		pos = self.file.tell()
		ch = self.file.read(1)
		if ch is ' ' or ch is '\t' or ch is '\n':
			if ch is '\n':
				self.line_number += 1
			self._skip_whitespace()
		else:  # Comments and other stuff
			if ch is '#':  # Octothope denotes a line comment
				while ch is not '\n':
					ch = self.file.read(1)
				self.file.seek(self.file.tell() - 1)
				self._skip_whitespace()
			else:
				self.file.seek(pos)

	def _lex_string(self):
		string = ""
		self.file.read(1)  # Skip the "
		ch = self.file.read(1)
		while ch is not '\"':
			string += ch
			ch = self.file.read(1)
		# string += ch

		return Lexeme(STRING, str(string))

	def _lex_identifier(self):
		id_ = ""
		ch = self.file.read(1)
		while ch.isalpha() or ch.isdigit() or ch is '_':
			id_ += ch
			ch = self.file.read(1)
		if ch is not '':
			self.file.seek(self.file.tell() - 1)

		if id_ == "return":
			return Lexeme(RETURN, id_)
		elif id_ == "def":
			return Lexeme(DEF, DEF)
		elif id_ == "if":
			return Lexeme(IF, IF)
		elif id_ == "fi":
			return Lexeme(FI, FI)
		elif id_ == "then":
			return Lexeme(THEN, THEN)
		elif id_ == "do":
			return Lexeme(DO, DO)
		elif id_ == "end":
			return Lexeme(END, END)
		elif id_ == "done":
			return Lexeme("DONE", id_)
		elif id_ == "elif":
			return Lexeme(ELIF, ELIF)
		elif id_ == "else":
			return Lexeme(ELSE, ELSE)
		elif id_ == "true":
			return Lexeme(BOOLTRUE, BOOLTRUE)
		elif id_ == "false":
			return Lexeme(BOOLFALSE, BOOLFALSE)
		elif id_ == "null":
			return Lexeme(NULL, NULL)
		elif id_ == "for":
			return Lexeme(FOR, FOR)
		elif id_ == "while":
			return Lexeme(WHILE, WHILE)
		elif id_ == "class":
			return Lexeme(CLASS, CLASS)
		elif id_ == "array":
			return Lexeme(ARRAY, ARRAY)
		elif id_ == "print":
			return Lexeme(PRINT, PRINT)
		else:
			return Lexeme(ID, id_)

	def _lex_digit(self):
		digit = ""
		ch = self.file.read(1)
		is_real = False
		while ch.isdigit() or ch is '.' or ch is '-':
			if ch is '.':
				is_real = True
			digit += ch
			ch = self.file.read(1)
		if ch is not '':
			self.file.seek(self.file.tell() - 1)

		if is_real:
			try:
				newReal = float(digit)
				return Lexeme(REAL, newReal)
			except:
				print("Error on line ", self.line_number, ": could not create REAL from '", digit, "'\n ", sep='')
				exit(25)
		else:
			try:
				newInt = int(digit)
				return Lexeme(INTEGER, newInt)
			except:
				print("Error on line ", self.line_number, ": could not create INT from '", digit, "'\n ", sep='')
				exit(25)
