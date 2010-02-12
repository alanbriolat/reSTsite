import docutils
import pygments
import pygments.lexers
import pygments.formatters

pygments_formatter = pygments.formatters.HtmlFormatter()

def pygments_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):
    """
    Docutils ReST directive for Pygments syntax highlighting

    Adapted from http://www.djangosnippets.org/snippets/36/
    """
    try:
        lexer = pygments.lexers.get_lexer_by_name(arguments[0])
    except ValueError:
        lexer = pygments.lexers.get_lexer_by_name('text')
    parsed = pygments.highlight(u'\n'.join(content), lexer, pygments_formatter)
    return [docutils.nodes.raw('', parsed, format='html')]
pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1

docutils.parsers.rst.directives.register_directive('code', pygments_directive)
