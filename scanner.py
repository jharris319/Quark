from lexer import *


def scanner(filename):
	i = Lexer(filename)
	token = i.lex()
	while token.type_ is not "EOF":
		print(token.type_, token.value, sep="\t|\t")
		token = i.lex()