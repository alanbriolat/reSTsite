import logging
import os.path
import yaml

import reSTsite.handlers
import reSTsite.templates
import reSTsite.filesystem as fs
from reSTsite.actions import CopyAction

class Site:

    def __init__(self, root):
        """
        Constructor: load configuration, load file handlers
        """
        self.log = logging.getLogger('reSTsite.Site')
        self.root = root
        
        configpath = os.path.join(self.root, '_config.yaml')
        if not os.path.exists(configpath):
            self.log.warning('Configuration not found: ' + configpath)
            self.config = dict()
        else:
            self.log.info('Loading configuration: ' + configpath)
            self.config = yaml.load(open(configpath, 'r'))

        reSTsite.handlers.load_handlers(['html', 'rst'])
        self.handlers = reSTsite.handlers.get_extension_handlers(self)

        self.tpl = reSTsite.templates.TemplateEngine('_templates')


    def process(self):
        for (fullpath, relpath, ext) in fs.walk(self.root):
            if ext in self.handlers:
                action = self.handlers[ext].process(relpath)
            else:
                action = CopyAction(self, relpath)
            action.process()
