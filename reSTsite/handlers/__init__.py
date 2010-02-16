import itertools
import sys
import os.path
import re
import logging
log = logging.getLogger('reSTsite.handlers')

from reSTsite import settings


class Handler(object):
    """
    File handler base class

    Exists primarily for collecting subclasses (actual file handlers).
    """
    # File extensions this handler handles
    EXTS = ()
    # Destination file extension
    EXT_DEST = '.html'

    # Get date from filename - if matched (year, month, day) = group(2, 5, 7)
    regex_metadata_filename = re.compile(
            r"""^
                # Date
                ((?P<year>\d{4})(-(?P<month>\d{2})(-(?P<day>\d{2}))?)?\W+)?
                # Slug/title
                (?P<slug>.+)
                $""", re.X)
    regex_metadata_directory = re.compile(
            r"""^
                # Tags
                (?P<tags>.*?)
                # Date
                (/?(?P<year>\d{4})(/(?P<month>\d{2})(/(?P<day>\d{2}))?)?)?
                $""".replace('/', os.path.sep), re.X)


    def __init__(self, fullpath, relpath):
        self.fullpath = fullpath
        self.relpath = relpath


    def get_target_path(self):
        return os.path.splitext(self.relpath)[0] + self.EXT_DEST

    
    def get_path_metadata(self):
        """
        Attempt to extract metadata from the path
        """
        # Extract metadata from directory name
        dir_metadata = self.regex_metadata_directory.search(
                os.path.dirname(self.relpath))
        dir_metadata = dir_metadata.groupdict()
        # Sanitise directory metadata
        dir_metadata['tags'] = set(dir_metadata['tags'].split(os.path.sep))
        # Extract metadata from filename
        file_metadata = self.regex_metadata_filename.search(
                os.path.basename(self.relpath))
        file_metadata = file_metadata.groupdict()
        # Sanitise file metadata
        file_metadata['slug'] = os.path.splitext(file_metadata['slug'])[0]
        # Merge metadata
        dir_metadata.update(file_metadata)
        # Strip out empty metadata
        for k, v in dir_metadata.items():
            if not v:
                del dir_metadata[k]
        return dir_metadata


    def to_context(self):
        """
        Build a context dictionary

        Get the context dictionary for this file.  Options are overridden in the
        following priority order (lowest to highest):

            settings['defaults']
            path metadata
            document parts
            document metadata
        """
        context = settings.get('defaults', dict()).copy()
        context.update(self.get_path_metadata())
        context.update(self.get_parts())
        context.update(self.get_metadata())
        context['settings'] = settings
        return context


    def load_string(self):
        return open(self.fullpath, 'r').read()


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
