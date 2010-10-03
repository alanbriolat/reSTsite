import os.path
import re
import shutil

from reSTsite.processor import Processor
from reSTsite.file_processors.docutils import RestructuredText
from reSTsite.file_processors.jinja2 import Jinja2Output, Jinja2Processor


class TargetPathPrefix(Processor):
    def __init__(self, prefix):
        self.prefix = prefix

    def process(self, f):
        f['target'] = os.path.join(self.prefix, f['target'])


class PathMetadata(Processor):
    FILENAME_METADATA_REGEX = re.compile(
        r"""^
            # Date
            ((?P<year>\d{4})(-(?P<month>\d{2})(-(?P<day>\d{2}))?)?\W+)?
            # Slug
            (?P<slug>.+)
            $""", re.X)

    def process(self, f):
        filemeta = self.FILENAME_METADATA_REGEX.search(os.path.splitext(f.basename)[0]).groupdict()
        f.update(filemeta)


class TargetFromMetadata(Processor):
    def __init__(self, pattern):
        self.pattern = pattern

    def process(self, f):
        f['target'] = self.pattern % f


class PassthroughProcessor(Processor):
    def generate(self, f):
        f.open_dest()
        shutil.copy(f.abs_sourcepath, f.abs_destpath)
