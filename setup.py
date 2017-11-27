"""This is setup.py of copan core"""

from setuptools import setup

# for developers: recommended way of installing is to run in this directory
# pip install -e .
# This creates a link insteaed of copying the files, so modifications in this directory are modifications in the installed package.

setup(name="pycopancore",
      version="0.0.0",
      description="to be added",
      url="to be added",
      author="Copan-group @ PIK",
      author_email="to be added",
      license="to be added",
      packages=["pycopancore"],
      install_requires=[
          "numpy>=1.11.0",
          "scipy>=0.17.0",
          "sympy>=1.0",
          "blist>=1.3.6",
          "profilehooks"

      ],
      zip_safe=False # see http://stackoverflow.com/questions/15869473/what-is-the-advantage-of-setting-zip-safe-to-true-when-packaging-a-python-projec
      )
