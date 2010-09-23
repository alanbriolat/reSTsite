import os.path
import re

from reSTsite.file_processors.docutils import RestructuredText
from reSTsite.file_processors.jinja2 import Jinja2Output


class TargetPathPrefix:
    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, f):
        f['target'] = os.path.join(self.prefix, f['target'])


class PathMetadata:
    FILENAME_METADATA_REGEX = re.compile(
        r"""^
            # Date
            ((?P<year>\d{4})(-(?P<month>\d{2})(-(?P<day>\d{2}))?)?\W+)?
            # Slug
            (?P<slug>.+)
            $""", re.X)

    def __init__(self):
        pass

    def __call__(self, f):
        filemeta = self.FILENAME_METADATA_REGEX.search(os.path.splitext(f.basename)[0]).groupdict()
        f.update(filemeta)


class TargetFromMetadata:
    def __init__(self, pattern):
        self.pattern = pattern

    def __call__(self, f):
        f['target'] = self.pattern % f
