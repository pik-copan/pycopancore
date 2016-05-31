# pycopancore
Python World-Earth modelling framework

Candidates for speeding up Python code: cython, numba, ...


## Tests
We are using the python testing framework [pytest](http://pytest.org/latest/) with [pep8](https://pypi.python.org/pypi/pytest-pep8) style guide and [pyflakes](https://pypi.python.org/pypi/pytest-flakes) error checking. Please write corresponding unittests while developing and make sure that all test pass by executing
```
py.test
```
in the root of the project tree.

Requires
* pytest
* pytest-pep8
* pytest-flakes
* pytest-cov, to check of test coverage
