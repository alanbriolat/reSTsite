import os
from itertools import ifilter
import re


def hidden_dir_filter(d):
    """Check if a directory path is hidden.
    
    Return True if a directory should be hidden.  A directory is considered
    hidden if it starts with '.' or '_'.
    """
    return d.startswith('.') or d.startswith('_')


def visible_file_filter(f):
    """Check if a file path is visible.

    Return False if a file should be hidden.  A file is considered hidden if
    it starts with '.' or '_', or ends with '~'.
    """
    return not (f.startswith('.') or f.startswith('_') or f.endswith('~'))


class FS:
    def __init__(self, root):
        self.root = root

    def open(self, path, mode='r'):
        return open(os.path.join(self.root, path), mode)

    def _walk(self):
        for root, dirs, files in os.walk(self.root):
            # Remove hidden dirs from tree traversal
            for d in filter(hidden_dir_filter, dirs):
                dirs.remove(d)
            # Yield only visible files
            for f in ifilter(visible_file_filter, files):
                yield FSFile(self, os.path.relpath(os.path.join(root, f), self.root))

    def __iter__(self):
        return self._walk()


class FSFile:
    def __init__(self, fs, path):
        self.fs = fs
        self.path = path

    def open(self, path, mode='r'):
        return self.fs.open(path, mode)


def get_target_path(root, relpath, newext = None):
    if newext:
        relpath = os.path.splitext(relpath)[0] + newext
    return os.path.join(root, '_deploy', relpath)


# Get date and slug from filename
regex_metadata_filename = re.compile(
        r"""^
            # Date
            ((?P<year>\d{4})(-(?P<month>\d{2})(-(?P<day>\d{2}))?)?\W+)?
            # Slug/title
            (?P<slug>.+)
            $""", re.X)
# Get tags and date from directory
regex_metadata_directory = re.compile(
        r"""^
            # Tags
            (?P<tags>.*?)
            # Date
            (/?(?P<year>\d{4})(/(?P<month>\d{2})(/(?P<day>\d{2}))?)?)?
            $""".replace('/', os.path.sep), re.X)


def get_path_metadata(relpath):
    """
    Attempt to extract metadata from a path
    """
    # Extract metadata from directory
    dirmeta = regex_metadata_directory.search(os.path.dirname(relpath)).groupdict()
    # Sanitise tags
    dirmeta['tags'] = set(dirmeta['tags'].split(os.path.sep))
    # Extract metadata from filename
    filemeta = regex_metadata_filename.search(os.path.basename(relpath)).groupdict()
    # Remove file extension from slug
    filemeta['slug'] = os.path.splitext(filemeta['slug'])[0]
    # Merge metadata
    dirmeta.update(filemeta)
    # Strip empty entries
    for k, v in dirmeta.items():
        if not v:
            del dirmeta[k]
    return dirmeta


def walk(root_dir):
    """
    Walk the directory

    Traverse the directory, omitting "hidden" directories and files.  This
    function forms a generator which yields (fullpath, relpath, ext) tuples.
    """
    for root, dirs, files in os.walk(root_dir):
        # Prune hidden directories
        for d in filter(hidden_dir_filter, dirs):
            dirs.remove(d)
        # Prune hidden files
        for f in filter(hidden_file_filter, files):
            files.remove(f)
        # Iterate over every non-hidden file
        for f in files:
            fullpath = os.path.join(root, f)
            yield (os.path.join(root, f),
                   os.path.join(get_relpath(root_dir, root), f),
                   os.path.splitext(f)[1])


def copy(source, dest):
    """
    Copy a file, first creating the target directory if it doesn't exist
    """
    dirname = os.path.dirname(dest)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    shutil.copy(source, dest)


def create(dest, mode='w'):
    """
    Open the specified file for writing, creating the containing directory
    if necessary
    """
    dirname = os.path.dirname(dest)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return open(dest, mode)
