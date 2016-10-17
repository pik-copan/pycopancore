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
* pylama
* pytest-cov, to check of test coverage
(maybe more, let's see)

## Documentation
Create local html version of the docs in the `dos` directory with
```
> make html
```

to be extended ...
