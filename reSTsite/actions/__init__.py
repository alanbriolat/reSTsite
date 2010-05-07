import logging

import reSTsite.filesystem as fs


class CopyAction:
    log = logging.getLogger('reSTsite')

    def __init__(self, site, relpath):
        self.site = site
        self.relpath = relpath

    def process(self):
        dest = fs.get_target_path(self.site.root, self.relpath)
        self.log.info('Copying ' + self.relpath + ' to ' + dest)
        fs.copy(self.relpath, dest)


class JinjaAction:
    log = logging.getLogger('reSTsite')

    def __init__(self, site, relpath, context):
        self.site = site
        self.relpath = relpath
        self.context = context

    def process(self):
        dest = fs.get_target_path(self.site.root, self.relpath, '.html')
        self.log.info('Rendering ' + self.relpath + ' to ' + dest)
        output = self.site.tpl.render(self.context['meta']['layout'], self.context)
        fs.create(dest).write(output)
