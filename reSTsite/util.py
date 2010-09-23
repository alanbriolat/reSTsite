import sys
import fnmatch


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


class FunctionChain:
    def __init__(self, *args):
        self.funcs = []
        for f in args:
            if isinstance(f, FunctionChain):
                self.funcs.extend(f.funcs)
            else:
                self.funcs.append(f)

    def __call__(self, *args, **kwargs):
        print args
        for f in self.funcs:
            f(*args, **kwargs)
