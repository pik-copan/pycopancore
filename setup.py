"""This is setup.py of pycopancore"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2019 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from setuptools import setup, find_packages

# for developers: recommended way of installing is to run in this directory
# pip install -e .
# This creates a link insteaed of copying the files, so modifications in this directory are modifications in the installed package.

setup(name="pycopancore",
      version="0.0.0",
      description=("Reference implementation of the copan:CORE World-Earth "
                   "modelling framework"),
      url="https://github.com/pik-copan/pycopancore",
      author="copan group @ PIK",
      author_email="copan:CORE maintainers <core@pik-potsdam.de>",
      license="BSD 2-clause",
      packages=find_packages(),
      install_requires=[
          "numpy>=1.11.0",
          "scipy>=0.17.0",
          "sympy>=1.0",
          "matplotlib>=3.0",
          "plotly>=3.10",
          "h5py>=2.9",
          "networkx>=2.3",
          "blist>=1.3.6",
          "python-louvain>=0.9",
          "profilehooks",
          "pytest",
          "pylama",
          "pylint",
          "pytest-cov>=2.5.1",
          "pylama_pylint",
          "numba",
      ],
      zip_safe=False # see http://stackoverflow.com/questions/15869473/what-is-the-advantage-of-setting-zip-safe-to-true-when-packaging-a-python-projec
      )
