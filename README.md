# pycopancore

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14938316.svg)](https://doi.org/10.5281/zenodo.14938316)
[![CI](https://github.com/pik-copan/pycopancore/actions/workflows/check.yml/badge.svg)](https://github.com/pik-copan/pycopancore/actions) [![codecov](https://codecov.io/gh/pik-copan/pycopancore/graph/badge.svg)](https://codecov.io/gh/pik-copan/pycopancore)
[![PyPI version](https://badge.fury.io/py/pycopancore.svg)](https://badge.fury.io/py/pycopancore)

## Overview

pycopancore is a Python implementation of the copan:CORE modeling framework for building World-Earth (global social-ecological) models. The framework allows easy implementation of complex models by combining different environmental, social-metabolic, and cultural submodels using various modeling techniques including differential equations, stochastic and deterministic events.

## Installation

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

The package can be installed by downloading the repository and running:

```
$ pip install .
```
from the root directory of the package. This will automatically install all the required dependencies.

For developers, the recommended way of installing is to run in the package main directory:

```
$ pip install -e .
```

Or with development dependencies:

```
$ pip install -e .[dev]
```

This creates a link instead of copying the files, so modifications in this directory are modifications in the installed package.


### Running a model

To run one of the preconfigured models, execute a python script in the `studies` folder, for example
```bash
pip install pycopancore
```

### Documentation
Comprehensive documentation is available at: https://pik-copan.github.io/pycopancore

See [examples](./examples/) for examples on how to use the framework.

## Questions / Problems

In case of questions please contact core@pik-potsdam.de or [open an issue](https://github.com/pik-copan/pycopancore/issues/new).

## Contributing
Merge requests are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md).
For major changes, please open an issue first to discuss what you would like to
change.