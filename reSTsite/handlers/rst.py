from docutils.core import publish_parts
from docutils.parsers.rst import Directive, directives
from docutils import nodes
import yaml

from reSTsite.handlers import Handler
import reSTsite.filesystem as fs
from reSTsite.actions import JinjaAction

class RstHandler(Handler):
    EXTS = ('.rst', '.rest', '.restructuredtext')

    def process(self, relpath):
        parts = publish_parts(open(relpath, 'r').read(), writer_name='html')
        meta = self.site.config.get('defaults', dict()).copy()
        meta.update(fs.get_path_metadata(relpath))
        meta.update(MetadataDirective.get_metadata())

        context = self.get_default_context()
        context.update({
            'meta': meta,
            'title': parts['title'],
            'htmlmeta': parts['meta'],
            'htmlcontent': parts['html_body'],
        })
        return JinjaAction(self.site, relpath, context)



class MetadataDirective(Directive):
    """
    Crude hackish reST directive for YAML metadata
    """
    required_arguments = 0
    optional_arguments = 0
    has_content = True

    _current_metadata = dict()

    def run(self):
        text = '\n'.join(self.content)
        MetadataDirective._current_metadata = yaml.load(text)
        # Consume the input
        return []

    @staticmethod
    def get_metadata():
        """
        Get the most recent metadata, resetting the class state
        """
        meta = MetadataDirective._current_metadata
        MetadataDirective._current_metadata = dict()
        return meta

directives.register_directive('metadata', MetadataDirective)


try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter

    pygments_formatter = HtmlFormatter()

    class PygmentsDirective(Directive):
        """
        reST directive for syntax highlighting

        Adapted (loosely) from http://www.djangosnippets.org/snippets/36/
        """
        required_arguments = 1
        optional_arguments = 0
        has_content = True

        def run(self):
            try:
                lexer = get_lexer_by_name(self.arguments[0])
            except ValueError:
                # No lexer found, use text instead
                lexer = get_lexer_by_name('text')
            parsed = highlight(u'\n'.join(self.content),
                               lexer, pygments_formatter)
            return [nodes.raw('', parsed, format='html')]

    directives.register_directive('code', PygmentsDirective)

except ImportError:
    log.warning('Could not import Pygments - syntax highlighting unavailable')
