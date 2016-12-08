# pycopancore
Python World-Earth modelling framework

* responsible senior scientists: Jobst Heitzig & Jonathan F. Donges
* The versioning of pycopancore has been chosen to be administrated on the [github.com system](http://github.com/) as the future prospect of this model strongly encourages outside contributions. Any release version will be pushed on the inhouse versioning systems, [gitlab](http://gitlab.pik-potsdam.de/) and / or [svn](https://www.pik-potsdam.de/services/it/core/software-repositories/subversion/subversion).

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
Create local html version of the docs in the `docs` directory with
```
> make html
```

## Code of Good Practice
When Developing the Code, please follow the guidelines below:
* Use as many `assert` statements as possible, even if they are computationally expensive. For actual runs, these checks can be switched off using the `-O` flag of the Python Interpreter.
* Use static values as little as possible. Preferably define a variable in the header of the file instead.
* For every class/function write a proper docstring before committing.
* Use proper (and long) variable names. Auto-completion will help typing them.
* If a similar set of command is used twice, write a function for it right away.
* Design the metadata used in the Variable class according to the [CF conventions](http://cfconventions.org/).
* When writing class and method docstrings, already specify types and bounds for arguments and return values in the [sphinx-compatible PyContracts way](https://andreacensi.github.io/contracts/).

Later:
* Use [NetCDF, the CF conventions](http://cfconventions.org/) and [PIK's Typed Data Transfer](https://www.pik-potsdam.de/research/transdisciplinary-concepts-and-methods/tools/tdt/tdt) to store (input and) output data and share it with other models.
* Read and follow the ["Guidelines for Ensuring Good Scientific Modelling Practice at PIK"](https://www.pik-potsdam.de/intranet/scientific-life-pik/modelling-strategy).



to be extended ...
