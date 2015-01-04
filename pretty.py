from types import *


def pretty_printer(tree):
	if tree.type_ is "program":
		return print_program(tree)
	elif tree.type_ is "var_def":
		return print_var_def(tree)
	elif tree.type_ is PLUS:
		return print_plus(tree)
	elif tree.type_ is MINUS:
		return print_minus(tree)
	elif tree.type_ is MULTIPLY:
		return print_multiply(tree)
	elif tree.type_ is DIVIDE:
		return print_divide(tree)
	elif tree.type_ is EXPONENT:
		return print_exponent(tree)
	elif tree.type_ is MODULUS:
		return print_modulus(tree)
	elif tree.type_ is IF:
		return print_if(tree)
	elif tree.type_ is "opt_elif":
		return print_opt_elif(tree)
	elif tree.type_ is "opt_else":
		return print_opt_else(tree)
	elif tree.type_ is LT:
		return print_lt(tree)
	elif tree.type_ is GT:
		return print_gt(tree)
	elif tree.type_ is LTE:
		return print_lte(tree)
	elif tree.type_ is GTE:
		return print_gte(tree)
	elif tree.type_ is NOTEQUAL:
		return print_notequal(tree)
	elif tree.type_ is EQUALITY:
		return print_equality(tree)
	elif tree.type_ is "block":
		return print_block(tree)
	elif tree.type_ is PRINT:
		return print_print(tree)
	elif tree.type_ is WHILE:
		return print_while(tree)
	elif tree.type_ is "statement_list":
		return print_statement_list(tree)
	elif tree.type_ is ASSIGN:
		return print_assign(tree)
	elif tree.type_ is ID:
		return print_ID(tree)
	elif tree.type_ is INTEGER:
		return print_integer(tree)
	elif tree.type_ is BOOLTRUE:
		return print_booltrue(tree)
	elif tree.type_ is BOOLFALSE:
		return print_boolfalse(tree)
	elif tree.type_ is ARRAY:
		return print_array(tree)
	elif tree.type_ is "func_def":
		return print_func_def(tree)
	elif tree.type_ is RETURN:
		return print_return(tree)
	elif tree.type_ is "param_list":
		return print_param_list(tree)
	elif tree.type_ is "func_call":
		return print_func_call(tree)
	elif tree.type_ is "class_def":
		return print_class(tree)


def print_program(tree):
	pretty_printer(tree.left)
	if tree.right is not None:
		return pretty_printer(tree.right)


def print_var_def(tree):
	if tree.right.type_ is INTEGER or tree.right.type_ is REAL or tree.right.type_ is STRING or tree.right.type_ is ID:
		print("$", tree.left.value, " = ", tree.right.value, sep='')
	else:
		print("$", tree.left.value, " = ", pretty_printer(tree.right), sep='')


def print_plus(tree):
	if tree.right.type_ is INTEGER or tree.right.type_ is REAL:
		return str(tree.left.value) + " + " + str(tree.right.value)
	else:
		return str(tree.left.value) + " + " + str(pretty_printer(tree.right))


def print_minus(tree):
	if tree.right.type_ is INTEGER or tree.right.type_ is REAL:
		return str(tree.left.value) + " - " + str(tree.right.value)
	else:
		return str(tree.left.value) + " - " + str(pretty_printer(tree.right))


def print_multiply(tree):
	if tree.right.type_ is INTEGER or tree.right.type_ is REAL:
		return str(tree.left.value) + " * " + str(tree.right.value)
	else:
		return str(tree.left.value) + " * " + str(pretty_printer(tree.right))


def print_divide(tree):
	if tree.right.type_ is INTEGER or tree.right.type_ is REAL:
		return str(tree.left.value) + " / " + str(tree.right.value)
	else:
		return str(tree.left.value) + " / " + str(pretty_printer(tree.right))


def print_exponent(tree):
	if tree.right.type_ is INTEGER or tree.right.type_ is REAL:
		return str(tree.left.value) + " ^ " + str(tree.right.value)
	else:
		return str(tree.left.value) + " ^ " + str(pretty_printer(tree.right))


def print_modulus(tree):
	if tree.right.type_ is INTEGER or tree.right.type_ is REAL:
		return str(tree.left.value) + " % " + str(tree.right.value)
	else:
		return str(tree.left.value) + " % " + str(pretty_printer(tree.right))


def print_if(tree):
	glue = tree.left
	print("if (", pretty_printer(glue.left), ") then", sep='')
	pretty_printer(glue.right)		# if body
	pretty_printer(tree.right)		# elifs
	opt_else = tree.right			# else
	while opt_else.right is not None:
		opt_else = opt_else.right
	pretty_printer(opt_else)
	print("fi")


def print_opt_elif(tree):
	glue = tree.left
	if glue.type_ is EPSILON:
		return
	print("elif (", pretty_printer(glue.left), ") then", sep='')
	pretty_printer(glue.right)
	if tree.right.type_ is "opt_elif":
		pretty_printer(tree.right)


def print_opt_else(tree):
	if tree.left.type_ is EPSILON:
		return
	print("else")
	pretty_printer(tree.left)


def print_lt(tree):
	return str(tree.left.value) + " < " + str(tree.right.value)


def print_gt(tree):
	return str(tree.left.value) + " > " + str(tree.right.value)


def print_lte(tree):
	return str(tree.left.value) + " <= " + str(tree.right.value)


def print_gte(tree):
	return str(tree.left.value) + " >= " + str(tree.right.value)


def print_notequal(tree):
	return str(tree.left.value) + " != " + str(tree.right.value)


def print_equality(tree):
	return str(tree.left.value) + " == " + str(tree.right.value)


def print_block(tree):
	return pretty_printer(tree.left)


def print_print(tree):
	if tree.left.type_ is STRING:
		print("print(\"" + str(tree.left.value) + "\")")
	else:
		print("print(" + str(tree.left.value) + ")")


def print_while(tree):
	print("while (" + pretty_printer(tree.left) + ") do")
	pretty_printer(tree.right)


def print_statement_list(tree):
	pretty_printer(tree.left)
	if tree.right is not None:
		return pretty_printer(tree.right)


def print_assign(tree):
	print(tree.left.value, " = ", pretty_printer(tree.right), sep='')


def print_ID(tree):
	return tree.value


def print_integer(tree):
	return tree.value


def print_array(tree):
	if tree.right is None:
		return str("array[" + str(tree.left.value) + "]")
	else:
		print(str(tree.left.value) + "[" + str(tree.right.value) + '] = ' + str(tree.right.left.left.value))


def print_booltrue(tree):
	return True


def print_boolfalse(tree):
	return False


def print_func_def(tree):
	if tree.right.type_ is EPSILON:
		print("def " + str(tree.left.value) + "()")
		pretty_printer(tree.right.right)
		print("end")
	else:
		print("def " + str(tree.left.value) + "(" + str(pretty_printer(tree.right)) + ")")
		param_list = tree.right
		while param_list.right.type_ is not "block":
			param_list = param_list.right
		pretty_printer(param_list.right)
		print("end")


def print_func_call(tree):
	if tree.right.type_ is EPSILON:
		print(str(tree.left.value) + "()")
	else:
		print(tree.right.type_)
		print(str(tree.left.value) + "(" + str(print_param_list(tree.right)) + ")")


def print_return(tree):
	print("return " + pretty_printer(tree.left))


def print_param_list(tree):
	val = str(pretty_printer(tree.left))
	if tree.right is not None and tree.right.type_ is not "block":
		val += ", "
		val += pretty_printer(tree.right)
	return val


def print_class(tree):
	print("class: " + str(tree.left.value))
	print_program(tree.right)