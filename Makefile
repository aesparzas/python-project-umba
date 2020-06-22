
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

test_unit:
	@echo "Running tests"
	python -m unittest discover -p "*.py" -s tests

server:
	@echo "Running server..."
	@export FLASK_APP=app && flask run

test: test_unit report

style_test: flakes pep8
