import logging
log = logging.getLogger('reSTsite.handlers.Jinja')

from reSTsite.handlers import Handler


class JinjaHandler(Handler):
    EXTS = ('.html', )

    def __init__(self):
        pass

    def render_from_file(self, source):
        pass
