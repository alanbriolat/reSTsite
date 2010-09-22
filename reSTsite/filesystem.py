import fnmatch
import os.path
from itertools import ifilter, imap
from functools import partial
import logging
_log = logging.getLogger('reSTsite.filesystem')

import util


DEFAULTS = {
    'exclude': ('.*', '_*', '*~'),
    'include': ('.htaccess',),
    'recursive': True,
    'file_processors': (),
    'dir_processors': (),
}


class Directory:
    def __init__(self, site, path):
        self.site = site
        self.path = path

    def fullpath(self, path):
        return os.path.join(self.path, path)


class SourceDirectory(Directory):
    def __init__(self, site, path, settings):
        Directory.__init__(self, site, path)

        self.settings = DEFAULTS.copy()
        self.settings.update(settings)

        self.file_processors = list()
        for pattern, processor, kwargs in self.settings['file_processors']:
            cls = util.load_processor(processor)
            self.file_processors.append((pattern, cls(**kwargs)))

        self.dir_processors = list()
        for processor, kwargs in self.settings['dir_processors']:
            cls = util.load_processor(processor)
            self.dir_processors.append(cls(**kwargs))

    def _visible_filter(self, path):
        """Check if a file path should be visible."""
        path = os.path.basename(path)
        # If path matches an include, overrides everything else
        if util.fnmatchany(path, self.settings['include']):
            return True
        # If path matches an exclude, hide it
        if util.fnmatchany(path, self.settings['exclude']):
            return False
        # By default, visible
        return True

    def _scan_non_recursive(self):
        return ifilter(self._visible_filter,
                       ifilter(os.path.isfile,
                               imap(partial(os.path.join, self.path),
                                    os.listdir(self.path))))

    def _scan_recursive(self):
        for root, dirs, files in os.walk(self.path):
            dirs[:] = filter(self._visible_filter, dirs)
            for f in ifilter(self._visible_filter, files):
                yield os.path.relpath(os.path.join(root, f), self.path)

    def process_files(self):
        if self.settings['recursive']:
            files = self._scan_recursive()
        else:
            files = self._scan_non_recursive()
        self.files = map(partial(File, self), files)

        for f in self.files:
            for pattern, processor in self.file_processors:
                if fnmatch.fnmatch(f.basename, pattern):
                    processor(f)

        print self.files

    def process(self):
        self.process_files()

    def generate_files(self):
        pass

    def generate(self):
        pass


class File(dict):
    def __init__(self, directory, path):
        dict.__init__(self)

        self.directory = directory
        self.path = path

        self['target'] = self.path
        self['ext'] = os.path.splitext(self.path)[1]

    @property
    def fullpath(self):
        return self.directory.fullpath(self.path)

    @property
    def basename(self):
        return os.path.basename(self.path)
