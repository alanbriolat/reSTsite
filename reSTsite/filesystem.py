import fnmatch
import os
import os.path
from itertools import ifilter
from functools import partial
import logging
_log = logging.getLogger('reSTsite.filesystem')

import util


DEFAULTS = {
    'path': '',
    'exclude': ('.*', '_*', '*~'),
    'include': ('.htaccess',),
    'recursive': True,
    'file_processors': (),
    'dir_processors': (),
}


class Directory(dict):
    """A directory, with a path relative to ``site['SITE_URL']``."""
    def __init__(self, site, path):
        self.site = site
        self.path = path

    def sourcepath(self, path):
        """Get path relative to site root from path relative to directory root."""
        return os.path.join(self.path, path)

    def abs_sourcepath(self, path=''):
        """Get absolute path from *path* relative to directory root."""
        return self.site.abs_sourcepath(self.sourcepath(path))


class SourceDirectory(Directory):
    def __init__(self, site, settings):
        self.site = site
        self.settings = DEFAULTS.copy()
        self.settings.update(settings)

        Directory.__init__(self, site, self.settings['path'])

        _log.debug('Configuring ' + self.abs_sourcepath())

        self.file_processors = list()
        for pattern, processors in self.settings['file_processors']:
            _log.debug('Adding processor chain for ' + pattern)
            self.file_processors.append((pattern, map(self._create_processor, processors)))

        self.dir_processors = map(self._create_processor, self.settings['dir_processors'])

    def _create_processor(self, processor):
        if isinstance(processor, tuple):
            processor, kwargs = processor
        else:
            kwargs = dict()
        cls = util.load_processor(processor)
        return cls(**kwargs)

    def _visible_filter(self, path):
        """Check if *path* should be visible.
        
        Decide if *path* should be visible, based on matching the basename part
        against include and exclude filters."""
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
        """Non-recursively generate file paths, relative to directory root."""
        for f in os.listdir(self.abs_sourcepath()):
            path = os.path.join(self.abs_sourcepath(), f)
            if os.path.isfile(path) and self._visible_filter(path):
                yield f

    def _scan_recursive(self):
        """Recursively generate file paths, relative to directory root."""
        for root, dirs, files in os.walk(self.abs_sourcepath()):
            relroot = os.path.relpath(root, self.abs_sourcepath())
            dirs[:] = filter(self._visible_filter, dirs)
            for f in ifilter(self._visible_filter, files):
                yield os.path.normpath(os.path.join(relroot, f))

    def process(self):
        _log.debug('Processing from ' + self.abs_sourcepath())
        self.process_files()
        self.process_dir()

    def process_files(self):
        if self.settings['recursive']:
            files = self._scan_recursive()
        else:
            files = self._scan_non_recursive()
        self.files = map(partial(File, self), files)

        for f in self.files:
            for pattern, processors in self.file_processors:
                if fnmatch.fnmatch(f.basename, pattern):
                    f.processors[:] = processors
                    break
            f.process()

    def process_dir(self):
        for p in self.dir_processors:
            p.process(self)

    def generate(self):
        _log.debug('Generating from ' + self.abs_sourcepath())
        self.generate_files()
        self.generate_dir()

    def generate_files(self):
        for f in self.files:
            f.generate()

    def generate_dir(self):
        for p in self.dir_processors:
            p.generate(self)


    def to_context(self):
        return dict()


class File(dict):
    def __init__(self, directory, path):
        dict.__init__(self)

        self.directory = directory
        self.site = directory.site
        self.path = path

        self['target'] = self.path
        self['ext'] = os.path.splitext(self.path)[1]

        self.processors = list()

    @property
    def sourcepath(self):
        """Source file path relative to site root."""
        return self.directory.sourcepath(self.path)

    @property
    def abs_sourcepath(self):
        """Absolute path to source file."""
        return self.directory.abs_sourcepath(self.path)

    @property
    def destpath(self):
        return self['target']

    @property
    def abs_destpath(self):
        return self.site.abs_destpath(self.destpath)

    @property
    def targetpath(self):
        """Target file path relative to deploy directory root."""
        return self['target']

    @property
    def basename(self):
        return os.path.basename(self.path)

    @property
    def url(self):
        return self.site.url(self['target'])

    def change_extension(self, ext):
        self['target'] = os.path.splitext(self['target'])[0] + ext
        self['ext'] = ext

    def process(self):
        _log.debug('Processing %s' % (self.sourcepath,))
        for p in self.processors:
            p.process(self)

    def generate(self):
        _log.debug('Generating %s -> %s' % (self.sourcepath, self.destpath))
        for p in self.processors:
            p.generate(self)

    def open_source(self, mode='r'):
        return open(self.abs_sourcepath, mode)

    def open_dest(self, mode='w'):
        dirname = os.path.dirname(self.abs_destpath)
        if not os.path.exists(dirname):
            os.makedirs(os.path.dirname(self.abs_destpath))
        return open(self.abs_destpath, mode)

    def to_context(self):
        context = self.copy()
        context['url'] = self.url
        context['dir'] = self.directory.to_context()
        return context

    def __repr__(self):
        return "<%s '%s'>" % (self.__class__.__name__, self.sourcepath)
