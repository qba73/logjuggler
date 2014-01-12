.PHONY: help clean clean-pyc clean-build list test coverage docs sdist

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 logjuggler test

test:
	py.test -v

coverage:
	coverage run --source logjuggler -m py.test
	coverage report

docs:
	rm -f docs/logjuggler.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ logjuggler
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

sdist: clean
	python setup.py sdist
	ls -l dist