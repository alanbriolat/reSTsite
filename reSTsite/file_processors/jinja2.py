from __future__ import absolute_import
from functools import partial
import os.path

from reSTsite.util import FunctionChain


def template_generate(self, targetdir):
    template = targetdir.site.tpl.get_template('layout/' + self['template'])
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


class Jinja2Processor:
    def __call__(self, f):
        metadata = f.site.tpl.get_metadata(f.fullpath)
        print metadata
