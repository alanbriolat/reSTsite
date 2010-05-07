import sys
import logging
log = logging.getLogger('reSTsite.handlers')


class Handler(object):
    """
    Handler base class

    A handler is something which knows how to process a particular kind of file.
    The type of a file is determined primarily by its extension.  The purpose of
    a handler is to create an Action for a file, which then is responsible for
    creating the necessary content in the deploy directory.
    """
    # File extensions this handler handles
    EXTS = ()

    def __init__(self, site):
        self.site = site


    def process(self, relpath):
        """
        Process a file, returning an Action
        """
        raise NotImplementedError


    def get_default_context(self):
        return {'config': self.site.config}


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


def get_extension_handlers(site):
    """
    Get a mapping of file extensions to Handler classes
    """
    extmap = dict()
    for h in find_handlers():
        hdlr = h(site)
        for ext in h.EXTS:
            if ext in extmap:
                log.warning('Overriding handler for %s' % ext)
            extmap[ext] = hdlr
            log.info('Registered %s for %s' % (hdlr, ext))
    return extmap
