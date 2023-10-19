# pycopancore
Reference implementation of the copan:CORE World-Earth modelling framework

copan:CORE is developed at the Potsdam Institute for Climate Impact Research.

An extensive documentation is found at https://pik-copan.github.io/pycopancore

Table of Contents:

1. [Introduction](#introduction)
2. [Disclaimer](#disclaimer)
3. [Quick start guide](#quick-start-guide)
    * [Installation](#installation)
    * [Documentation](#documentation)
    * [Code of good practice](#code-of-good-practice)
    * [Tests](#tests)
4. [Structure of the repository](#structure-of-the-repository)
5. [Licence and Development](#licence-and-development)

## Introduction

The pycopancore package is a python implementation of the copan:CORE modeling framework as described in [this paper](http://dx.doi.org/10.5194/esd-11-395-2020). The framework is designed to allow an easy implementation of World-Earth (i.e., global social-ecological) models by using different model components of environmental, social-metabolic or cultural submodels and combining them with newly developed components.
The implementation and simulation of World-Earth models within the framework can use  different types of modeling techniques such as differential equations, stochastic and deterministic events and therefore allows to compare different model and component types and implementations.

Reference: J.F. Donges*/J. Heitzig*, W. Barfuss, M. Wiedermann, J.A. Kassel, T. Kittel, J.J. Kolb, T. Kolster, F. Müller-Hansen, I.M. Otto, K.B. Zimmerer, and W. Lucht, Earth system modeling with endogenous and dynamic human societies: the copan:CORE open World-Earth modeling framework, Earth System Dynamics 11, 395–413 (2020), DOI: 10.5194/esd-11-395-2020, * The first two authors share the lead authorship.

pycopancore is developed at the Potsdam Institute for Climate Impact Research (PIK), Research Domains for Earth System Analysis and Complexity Science. Responsible senior scientists at PIK are [Jobst Heitzig](https://www.pik-potsdam.de/members/heitzig) & [Jonathan F. Donges.](https://www.pik-potsdam.de/members/donges)

Contact: core@pik-potsdam.de
Website: www.pik-potsdam.de/copan/software

<img src="https://www.pik-potsdam.de/members/heitzig/public/core-1.png" width="1280">

## Disclaimer

This software is provided for free as a beta version still under active development. It has not been completely tested and can therefore not guarantee  error-free functioning. Please help us further improving the code by reporting possible bugs via the github issue tracker!

## Quick start guide

### Installation

For running pycopancore, an installation with python > 3.6 with some additional packages is required.

An easy way to install python is to use the Anaconda environment ([https://www.anaconda.com/download/](https://www.anaconda.com/download/)).

The package can be installed by downloading the repository and and running the setup.py script with

```
$ pip install
```
from the root directory of the package. The script should automatically install all the required and missing packages.

For developers, the recommended way of installing is to run in the package main directory

```
$ pip install -e .
```

This creates a link instead of copying the files, so modifications in this directory are modifications in the installed package.


### Running a model

To run one of the preconfigured models, execute a python script in the `studies` folder, for example
```bash
python run_seven_dwarfs.py
```

### Documentation

The documentation can be accessed under https://pik-copan.github.io/pycopancore and provides an introduction to the framework, its different entity and process types, a full documentation of the API as well as a step-by-step tutorial.

To create a local html version of the documentation, access the `docs` directory and type

```
> make html
```
The documentation can then be accessed under `docs/_build/html/index.html`.

To be able to create the automatic UML-Diagrams, [pylint](https://www.pylint.org/) and [graphviz](http://www.graphviz.org/) needs to be installed. To finally create the diagrams, use
```
> make uml
```

### Code of Good Practice

When contributing to the project, please follow the guidelines below:
* For every class/function write a proper docstring before committing.
* Use static values as little as possible. Preferably define a variable in the header of the file instead.
* For functions describing processes in the `model_components`, papers from the scientific literature that use these functional forms should be referenced in the code documentation.
* Use as many `assert` statements as possible, even if they are computationally expensive. For actual runs, these checks can be switched off using the `-O` flag of the Python Interpreter.
* Use proper (and long) variable names. Auto-completion will help typing them.
* If a similar set of command is used twice, write a function for it right away.
* Design the metadata used in the Variable class according to established catalogs like the [CF conventions](http://cfconventions.org/).
* When writing class and method docstrings, already specify types and bounds for arguments and return values in the [sphinx-compatible PyContracts way](https://andreacensi.github.io/contracts/).
* Follow the ["Guidelines for Ensuring Good Scientific Modelling Practice at PIK"](https://www.pik-potsdam.de/intranet/scientific-life-pik/modelling-strategy).

### Tests
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

## Structure of the repository

The code in the repository is organized into different subfolders:

**docs** contains a detailed description of the framework and scripts to compile API documentation of the code (see [Quick start guide/Documentation](#documentation)). Furthermore, it contains the material for the framework tutorials.

**examples** ??

**graphics** contains code to visualize model output.
 
**pycopancore** contains the main code of the framework, specifically:

**pycopancore/data_model** implements and specifies the underlying master data model for the different process taxa and provides a base for defining units and keeping them consistent.

**pycopancore/model_components** contains various subfolders, in which model components and their interfaces with other components are defined.

**pycopancore/models** contains code files that combine different model components to self-contained models. 

**pycopancore/private** implements classes that are needed for the correct plugging together of model components and other functionality for preparing the model for running. 

**pycopancore/process_types** contains the definitions for the different process types (events, steps, explicit and implicit equations, and ordinary differential equations).

**pycopancore/runners** contains implementation of model runner, that executes the model by integrating its processes.

**pycopancore/util** contains auxiliary functions.

**studies** accommodates the files for executing the models. These "run" files define parameter settings, initialize model entities and start the model runner.

**tests** comprises code to implement and run testing procedures of the implementation.

## Licence and Development

pycopancore is licenced under the BSD 2-Clause License.
See the `LICENCE` file for further information.

The versioning of pycopancore has been chosen to be administrated on the [github.com system](http://github.com/) as the future prospect of this model strongly encourages outside contributions. Any release version will be pushed on the inhouse versioning systems, [gitlab](http://gitlab.pik-potsdam.de/) and / or [svn](https://www.pik-potsdam.de/services/it/core/software-repositories/subversion/subversion).

Candidates for speeding up Python code: cython, numba, ...

