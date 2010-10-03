import imp
import os.path
import logging
_log = logging.getLogger('reSTsite.site')

from filesystem import SourceDirectory, Directory
from templating import reSTsiteEnvironment


class Site(dict):
    """Class representing a site configuration.

    A :class:`Site` object represents the site with it's source root at
    *site_path* and settings at *config*.  The class has a dictionary interface
    for accessing settings, with settings from the configuration file
    overriding defaults.  Settings expected to be in the configuration file are
    in uppercase.  All paths are relative to *site_path* except *config* (but
    *config* defaults to :file:`<site_path>/_settings.py`).
    """
    def __init__(self, site_path='', config=None):
        # Default configuration path
        if config is None:
            config = os.path.join(site_path, '_settings.py')
        # Initialise dict with defaults
        dict.__init__(self, {
            'SITE_PATH': site_path,
            'SITE_URL': '/',
            'DEPLOY_DIR': '_deploy',
            'TEMPLATE_DIR': '_templates',
            'CONTENT': (),
            'STYLESHEETS': (),
        })
        self.update(self._load_settings(config))
        # Setup templating environment
        self.tpl = reSTsiteEnvironment(self.abs_sourcepath(), 
                                       self.abs_sourcepath(self['TEMPLATE_DIR']),
                                       {'site': self})

        self.content = dict()
        for k, v in self['CONTENT'].iteritems():
            self.content[k] = SourceDirectory(self, v)

    def abs_sourcepath(self, path=''):
        """Get absolute path from *path* relative to site root."""
        return os.path.abspath(os.path.join(self['SITE_PATH'], path))

    def abs_destpath(self, path):
        """Get destination/output file path from a site-relative *path*."""
        return os.path.abspath(os.path.join(self['SITE_PATH'],
                                            self['DEPLOY_DIR'],
                                            path))

    def url(self, path):
        """Get URL from site-relative path."""
        return self['SITE_URL'].rstrip('/') + '/' + path.lstrip('/')

    def process(self):
        for key, d in self.content.iteritems():
            d.process()

    def generate(self):
        for key, d in self.content.iteritems():
            d.generate()

    @staticmethod
    def _settings_filter(kv):
        return not kv[0].startswith('_') and kv[0].upper() == kv[0]

    @staticmethod
    def _load_settings(filename):
        if not os.path.exists(filename):
            _log.critical('Settings file %s does not exist' % (filename, ))
            exit(1)
        try:
            mod = imp.load_source('settings', filename)
        except Exception:
            _log.critical('The settings file %s contains errors that prevent '
                    'it from being loaded as a Python module' % (filename,))
            raise
        else:
            _log.info('Loaded settings from ' + filename)
            return dict(filter(Site._settings_filter, mod.__dict__.iteritems()))
