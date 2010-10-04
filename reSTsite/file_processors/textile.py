from __future__ import absolute_import

import textile

from reSTsite.processor import Processor


class TextileProcessor(Processor):
    def generate(self, f):
        f['htmlbody'] = textile.textile(open(f.abs_sourcepath, 'r').read())
