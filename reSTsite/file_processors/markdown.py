from __future__ import absolute_import

import markdown

from reSTsite.processor import Processor


class MarkdownProcessor(Processor):
    def generate(self, f):
        f['htmlbody'] = markdown.markdown(open(f.abs_sourcepath, 'r').read(),
                                          extensions=['codehilite(css_class=highlight)'])
