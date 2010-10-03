import sys
import fnmatch
from itertools import izip, tee


def load_processor(name):
    """Load and return a processor class by name."""
    (module_name, sep, processor) = name.rpartition('.')
    __import__(module_name)
    module = sys.modules[module_name]
    return getattr(module, processor)


def fnmatchany(path, patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)
