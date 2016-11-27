# pycopancore
Python World-Earth modelling framework

Candidates for speeding up Python code: cython, numba, ...


## Tests
We are using the python testing framework [pytest](http://pytest.org/latest/) with [pylama](https://github.com/klen/pylama) for style and error checking. Please write corresponding unittests while developing and make sure that all test pass by executing
```
py.test
```
in the root of the project tree.

Requires
* pytest
* pylama
* pylint
* pylama_pylint
* pytest-cov, to check of test coverage


## Documentation
Create local html version of the docs in the `dos` directory with
```
> make html
```

## Code of Good Practice
When Developing the Code, please follow the guidelines below:
* Use as many `assert` statements as possible, even if they are computationally expensive. For actual runs, these checks can be switched off using the `-O` flag of the Python Interpreter.
* Use Type Hints ([PEP 484](https://www.python.org/dev/peps/pep-0484/)) if possible and check your code for consistency with [mypy](http://mypy-lang.org/) before committing.
* Use static values as little as possible. Preferably define a variable in the header of the file instead.
* For every class/function write a proper docstring before committing.
* Use proper (and long) variable names. Auto-completion will help typing them.
* If a similar set of command is used twice, write a function for it right away.

to be extended ...
