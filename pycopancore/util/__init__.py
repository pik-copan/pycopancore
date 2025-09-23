from .. import config
from .functions import *
from .seeding import *

# profiling:

try:
    from line_profiler import LineProfiler

    class _Profile(object):

        def __init__(self):
            self.profile = LineProfiler()

        def __call__(self, f):
            return self.profile(f) if config.profile else f

        def __getattr__(self, key):
            return getattr(self.profile, key)

except ImportError:

    class _Profile(object):

        def __call__(self, f):
            if config.profile:
                print("INFO: line_profiler not available")
            return f

        def __getattr__(self, key):
            print("INFO: line_profiler not available")
            return None


profile = _Profile()
