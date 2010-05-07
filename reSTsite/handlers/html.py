import logging
import yaml
import jinja2

from reSTsite.handlers import Handler
from reSTsite.actions import CopyAction, JinjaAction
import reSTsite.filesystem as fs

class HtmlHandler(Handler):
    EXTS = ('.htm', '.html')
    log = logging.getLogger('reSTsite.HtmlHandler')

    def process(self, relpath):
        contents = open(relpath, 'r').read()
        if contents.startswith('<!--metadata:'):
            startpos = len('<!--metadata:')
            endpos = contents.find('-->')
            if endpos == -1:
                self.log.error('Couldn\'t find end of metadata comment')
                return CopyAction(self.site, relpath)
            else:
                filemeta = yaml.load(contents[startpos:endpos])
                contents = contents[endpos + len('-->'):];
                meta = self.site.config.get('defaults', dict()).copy()
                meta.update(fs.get_path_metadata(relpath))
                meta.update(filemeta)
                context = self.get_default_context()
                context.update({
                    'meta': meta,
                    'title': meta.get('title', 'Untitled'),
                })
                output = jinja2.Template(contents).render(context)
                context.update({
                    'htmlcontent': output,
                })
                return JinjaAction(self.site, relpath, context)
        else:
            return CopyAction(self.site, relpath)
