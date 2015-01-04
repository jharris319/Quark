from pretty import *
from evaluator import *
import sys


def vis_tree(pt):
	fp = open("./graphviz/data.dot", "w")
	fp.write("digraph g {")
	fp.write("\n\tnode  [shape = record, height = .1];")
	node_helper(fp, pt, 1)
	connect_helper(fp, pt, 1)
	fp.write("\n}")
	fp.close()

	import os
	os.system("dot -Tpng ./graphviz/data.dot -o ./graphviz/data.png")


def node_helper(fp, pt, tag):
	if pt is not None:
		if pt.value is not None and pt.type_ is not 'lt' and pt.type_ is not 'gt' and pt.type_ is not 'lte' and pt.type_ is not 'gte':		# Fixed the string oddities
			fp.write("\n\tnode" + str(tag) + " [label = \"<f0> | <f1> " + str(pt.type_) + " " + str(pt.value) + " | <f2>\"];")
		elif pt.type_ is 'lt' or pt.type_ is 'gt' or pt.type_ is 'lte' or pt.type_ is 'gte':
			string_val = str(pt.value)
			string_val = "\\" + string_val
			fp.write("\n\tnode" + str(tag) + " [label = \"<f0> | <f1> " + str(pt.type_) + " " + string_val + " | <f2>\"];")
		else:
			fp.write("\n\tnode" + str(tag) + " [label = \"<f0> | <f1> " + str(pt.type_) + " | <f2>\"];")
		if pt.left is not None:
			node_helper(fp, pt.left, (tag * 2))
		if pt.right is not None:
			node_helper(fp, pt.right, ((tag * 2) + 1))


def connect_helper(fp, pt, tag):
	if pt is not None:
		if pt.left is not None:
			fp.write("\n\t\"node" + str(tag) + "\"")
			fp.write(":f0 -> \"node" + str((tag * 2)) + "\":f1;")
			connect_helper(fp, pt.left, (tag * 2))
		if pt.right is not None:
			fp.write("\n\t\"node" + str(tag) + "\"")
			fp.write(":f2 -> \"node" + str(((tag * 2) + 1)) + "\":f1;")
			connect_helper(fp, pt.right, ((tag * 2) + 1))

# # Lexer Only
# from scanner import *
# scanner("./source/source-functions")

# # Recognizer (see graphviz)
# i = Recognizer(sys.argv[1])
# pt = i.program()
# vis_tree(pt)
# print("Generated tree...\nsee ./graphviz/data.png")

# Pretty Printer (see graphviz)
i = Recognizer(sys.argv[1])
pt = i.program()
vis_tree(pt)
pretty_printer(pt)

# # Evaluator
# i = Evaluator("./tests/testEval")
# vis_tree(i.tree)
# i.eval(i.tree, i.environment)