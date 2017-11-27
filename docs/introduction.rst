Introduction
============

... one framework to rule them all!
...................................

Python copan:CORE World-Earth modeling framework release version [...]

Table of Contents:
------------------

1. :ref:`intro`
2. :ref:`disclaimer`
3. :ref:`quickstart`
    * :ref:`installation`
    * :ref:`running`
    * :ref:`docu`
    * :ref:`CoC`
    * :ref:`test`
4. :ref:`licence`

.. _intro:

Introduction
............

The pycopancore package is a python implementation of the copan:CORE modeling framework as described in [include reference to framework description paper]. The framework is designed to allow an easy implementation of World-Earth (i.e., global social-ecological) models by using different model components of environmental, social-metabolic or cultural submodels and combining them with newly developed components.
The implementation and simulation of World-Earth models within the framework can use  different types of modeling techniques such as differential equations, stochastic and deterministic events and therefore allows to compare different model and component types and implementations.

pycopancore is developed at the Potsdam Institute for Climate Impact Research (PIK). Responsible senior scientists at PIK are [Jobst Heitzig](https://www.pik-potsdam.de/members/heitzig) & [Jonathan F. Donges.](https://www.pik-potsdam.de/members/donges)

.. _disclaimer:

Disclaimer
..........

This software is provided for free as a beta version still under active development. It has not been completely tested and can therefore not guarantee  error-free functioning. Please help us further improving the code by reporting possible bugs via the github issue tracker!

.. _quickstart:

Quick start guide
.................

.. _installation:

Installation
------------

For running pycopancore, an installation with python > 3.6 with some additional packages is required.

An easy way to install python is to use the Anaconda environment ([https://www.anaconda.com/download/](https://www.anaconda.com/download/)).

The package can be installed by downloading the repository and and running the setup.py script with

```
$ pip install
```
from the root directory of the package. The script should automatically install all the required and missing packages.

For developers, the recommended way of installing is to run in the package main directory

```
$ pip install -e
```

This creates a link instead of copying the files, so modifications in this directory are modifications in the installed package.

.. _running:

Running a model
---------------

To run one of the preconfigured models, execute a python script in the `studies` folder, for example
```bash
python run_seven_dwarfs.py
```

.. _docu:

Documentation
-------------

The documentation can be accessed under [insert link] and provides an introduction to the framework, its different entity and process types, a full documentation of the API as well as a step-by-step tutorial.

To create a local html version of the documentation, access the `docs` directory and type
```
> make html
```
The documentation can then be accessed under `docs/_build/html/index.html`.

To be able to create the automatic UML-Diagrams, [pylint](https://www.pylint.org/) and [graphviz](http://www.graphviz.org/) needs to be installed. To finally create the diagrams, use
```
> make uml
```

.. _CoC:

Code of Good Practice
---------------------

When contributing to the project, please follow the guidelines below:
* For every class/function write a proper docstring before committing.
* Use static values as little as possible. Preferably define a variable in the header of the file instead.
* For functions describing processes in the `model_components`, papers from the scientific literature that use these functional forms should be referenced in the code documentation.
* Use as many `assert` statements as possible, even if they are computationally expensive. For actual runs, these checks can be switched off using the `-O` flag of the Python Interpreter.
* Use proper (and long) variable names. Auto-completion will help typing them.
* If a similar set of command is used twice, write a function for it right away.
* Design the metadata used in the Variable class according to the [CF conventions](http://cfconventions.org/).
* When writing class and method docstrings, already specify types and bounds for arguments and return values in the [sphinx-compatible PyContracts way](https://andreacensi.github.io/contracts/).
* Write in code-of-conduct: Everything but "models" and "model_components" should be well described with docstrings"
* Consider the recommendations in the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for python code.

Additional guidelines:
* Staff of the Potsdam Institute for Climate Impact research, please read and follow the ["Guidelines for Ensuring Good Scientific Modelling Practice at PIK"](https://www.pik-potsdam.de/intranet/scientific-life-pik/modelling-strategy).
* Use [NetCDF, the CF conventions](http://cfconventions.org/) and [PIK's Typed Data Transfer](https://www.pik-potsdam.de/research/transdisciplinary-concepts-and-methods/tools/tdt/tdt) to store (input and) output data and share it with other models.

.. _test:

Tests
-----

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

.. _licence:

Licence and Development
.......................

pycopancore is licenced under the BSD 2-Clause License.
See the `LICENCE` file for further information.

The versioning of pycopancore has been chosen to be administrated on the [github.com system](http://github.com/) as the future prospect of this model strongly encourages outside contributions. Any release version will be pushed on the inhouse versioning systems, [gitlab](http://gitlab.pik-potsdam.de/) and / or [svn](https://www.pik-potsdam.de/services/it/core/software-repositories/subversion/subversion).

Candidates for speeding up Python code: cython, numba, ...
