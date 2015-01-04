Quark
-----

A programming language written in Python.

#### Overview ####

Quark currently contains a working grammar, lexer, recognizer, pretty printer, and the beginnings of an evaluator. Currently, the evaluator works for variable definitons, if statements, expressions, print statements, and logic expressions.


##### Parse Tree #####
![Parse Tree Example](https://github.com/jharris319/Quark/master/graphviz/data.png)


##### Syntax #####

###### Definitions ######
'''python
$string = "string"
$someString = "I'm a string"
$someInteger = 403
$someFloat = 4.03
$someAdd = 1 + 2 + 3
$someSub = 1 - 2 - 3
$someMult = 1 * 2 * 3
$someDiv = 2 / 3
$a = -2
$b = 3
'''

###### Statements ######
'''python
if (a != b) then
	print("foo")
elif (b != c) then
	print("bar")
else
	print("baz")
fi

while(a != b) do
	print("loop")
	if (a > 2) then
		a = b % a
	fi
end

print("hello world!")

return .234 * 333.999
,,,

###### Functions ######
,,,python
def baz()
	print("foo!")
end

def foo(var1, var2, var3)
	return (var1 + var2 + var3)
end

foo(5, roo, foo)
,,,