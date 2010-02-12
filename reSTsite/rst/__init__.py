import docutils.parsers.rst
from pygments_directive import pygments_directive

def register_directives():
    docutils.parsers.rst.directives.register_directive('code', pygments_directive)
