from lexeme import *


def cons(type_, left, right):
	tmp = Lexeme(type_)
	tmp.left = left
	tmp.right = right
	return tmp


def create():
	return extend(None, None, None)


def lookup(variable, env):
	while env is not None:
		table = env.left
		vars_ = table.left
		vals_ = table.right
		while vars_ is not None:
			if variable is vars_.left:
				return vals_.left
			vars_ = vars_.right
			vals_ = vals_.right
		env = env.right

	print("variable ", variable.value, " is undefined")
	exit(2)

	return None


def extend(variables, values, env):
	return cons("env", cons("value", variables, values), env)


def insert(variable, value, env):
	table = env.left
	table.left = cons("glue", variable, table.left)
	table.right = cons("glue", value, table.right)
	return value