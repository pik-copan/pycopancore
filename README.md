# pycopancore
reference implementation of the copan:CORE World-Earth modelling framework

* Responsible senior scientists: Jobst Heitzig & Jonathan F. Donges at the Potsdam Institute for Climate Impact Research.
* The versioning of pycopancore has been chosen to be administrated on the [github.com system](http://github.com/) as the future prospect of this model strongly encourages outside contributions. Any release version will be pushed on the inhouse versioning systems, [gitlab](http://gitlab.pik-potsdam.de/) and / or [svn](https://www.pik-potsdam.de/services/it/core/software-repositories/subversion/subversion).

copan:CORE is developed at the Potsdam Institute for Climate Impact Research.


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
Create local html version of the docs with [Sphinx](http://www.sphinx-doc.org/en/stable/)(version >= 1.6.3) in the `docs` directory with
```
> make html
```
To be able to create the automatic UML-Diagrams, [pylint](https://www.pylint.org/) and [graphviz](http://www.graphviz.org/) needs to be installed. To finally create the diagrams, use
```
> make uml
```

## Code of Good Practice
When Developing the Code, please follow the guidelines below:
* Use as many `assert` statements as possible, even if they are computationally expensive. For actual runs, these checks can be switched off using the `-O` flag of the Python Interpreter.
* Use static values as little as possible. Preferably define a variable in the header of the file instead.
* For every class/function write a proper docstring before committing.
* Use proper (and long) variable names. Auto-completion will help typing them.
* If a similar set of command is used twice, write a function for it right away.
* Design the metadata used in the Variable class according to established catalogs like the [CF conventions](http://cfconventions.org/).
* When writing class and method docstrings, already specify types and bounds for arguments and return values in the [sphinx-compatible PyContracts way](https://andreacensi.github.io/contracts/).
* Follow the ["Guidelines for Ensuring Good Scientific Modelling Practice at PIK"](https://www.pik-potsdam.de/intranet/scientific-life-pik/modelling-strategy).

## Installation

for developers: recommended way of installing is to run in the package main directory (where the setup.py is located):

$ pip install -e .

This creates a link insteaed of copying the files, so modifications in this directory are modifications in the installed package.



to be extended ...
