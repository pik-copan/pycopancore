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
* pytest-cov, to check of test coverage


## Documentation
Create local html version of the docs in the `dos` directory with
```
> make html
```

to be extended ...
