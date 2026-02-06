"""
This is the pycopancore package.
"""

try:
    from ._version import __version__
except ModuleNotFoundError:  # pragma: no cover
    # package is not installed
    __version__ = "0.8.3"

from pycopancore.model_components.base import (
    Individual,
    Group,
    SocialSystem,
    Cell,
    World,
    Environment,
    Metabolism,
    Culture,
)
