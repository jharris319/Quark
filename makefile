make:
	@echo "nothing to build"
	@echo ""
	python3 main.py

source-arrays:
	cat ./source/source-arrays

arrays:
	python3 main.py 

source-conditionals:
	cat ./source/source-conditionals

source-iteration:
	cat ./source/source-iteration

source-functions:
	cat ./source/source-functions

clean:
	rm -r __pycache__