import imp
import os.path
import logging
_log = logging.getLogger('reSTsite.site')

from filesystem import SourceDirectory, Directory


class Site:
    def __init__(self, options):
        self.options = options
        try:
            self.settings = imp.load_source('settings', options.config)
        except Exception:
            _log.critical('The settings file "%s" contains errors that prevent it '
                          'from being loaded as Python module' % (options.config,))
            raise

        self.directories = list()
        for path, settings in self.settings.CONTENT:
            d = SourceDirectory(self, os.path.join(options.site_path, path), settings)
            self.directories.append((path, d))

    def process(self):
        for path, d in self.directories:
            d.process()

    def generate(self):
        targetdir = Directory(self,
                              os.path.join(self.options.site_path,
                                           self.settings.DEPLOY_DIR))
        for path, d in self.directories:
            d.generate(targetdir)
