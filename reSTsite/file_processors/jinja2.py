from __future__ import absolute_import
from functools import partial
import os.path

from jinja2 import Environment, FileSystemLoader, PrefixLoader

from reSTsite.util import FunctionChain


class CustomEnvironment(Environment):
    def join_path(self, template, parent):
        return 'layout/' + template


def template_generate(self, targetdir):
    env = CustomEnvironment(loader=PrefixLoader({
            'layout':   FileSystemLoader(os.path.join(targetdir.site.options.site_path,
                                                      targetdir.site.settings.TEMPLATE_DIR)),
    }))
    template = env.get_template('layout/' + self['template'])
    output = template.render(self)
    print output


class Jinja2Output:
    def __init__(self, template, extension='.html'):
        self.template = template
        self.extension = extension

    def __call__(self, f):
        f['template'] = self.template
        f.change_extension(self.extension)
        f.generate = FunctionChain(f.generate, partial(template_generate, f))
