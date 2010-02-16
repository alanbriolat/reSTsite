import itertools
import sys
import logging
log = logging.getLogger('reSTsite.handlers')


class Handler(object):
    """
    File handler base class

    Exists primarily for collecting subclasses (actual file handlers).
    """
    # File extensions this handler handles
    EXTS = ()


def load_handlers(handlers):
    """
    Load handlers by importing their modules
    """
    for h in handlers:
        name = 'reSTsite.handlers.%s' % h
        try:
            log.info('Loading %s' % name)
            __import__(name)
            mod = sys.modules[name]
        except ImportError:
            log.error('Failed to load %s' % name)
            raise


def find_handlers():
    """
    Get all Handler classes
    """
    return Handler.__subclasses__()


def get_extension_handlers():
    """
    Get a mapping of file extensions to Handler classes
    """
    extmap = dict()
    for h in find_handlers():
        for ext in h.EXTS:
            if ext in extmap:
                log.warning('Overriding handler for %s' % ext)
            extmap[ext] = h
            log.info('Registered %s for %s' % (h, ext))
    return extmap
