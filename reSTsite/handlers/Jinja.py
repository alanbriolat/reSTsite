import logging
log = logging.getLogger('reSTsite.handlers.Jinja')

from reSTsite.handlers import Handler

from jinja2 import Environment, FileSystemLoader, PrefixLoader


class CustomEnvironment(Environment):
    def join_path(self, template, parent):
        """
        All includes/extends act as if prefixed by "layout/", no inclusion of
        other content
        """
        return 'layout/%s' % template


class JinjaHandler(Handler):
    EXTS = ('.html', )

    def __init__(self):
        pass

    def render_from_file(self, fullpath, relpath):
        env = CustomEnvironment(loader=PrefixLoader({
                    'layout':   FileSystemLoader('layout'),
                    'site':     FileSystemLoader('content')}))
        template = env.get_template('site/%s' % relpath)
        
        return template.render()
