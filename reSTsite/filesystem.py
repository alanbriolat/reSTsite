import os
import shutil
import re

def hidden_dir_filter(d):
    """
    Return True if the directory begins with . or _
    """
    return d.startswith('.') or d.startswith('_')


def hidden_file_filter(f):
    """
    Return True if the filename begins with . or _ or ends with ~
    """
    return hidden_dir_filter(f) or f.endswith('~')


def get_relpath(root_dir, path):
    """
    Find the relative path of some path contained within root_dir

    Adapted from:
    http://github.com/lakshmivyas/hyde/blob/master/hydeengine/path_util.py
    """
    relative = ''
    remaining = path
    while not remaining == root_dir:
        (remaining, part) = os.path.split(remaining)
        relative = os.path.join(part, relative)
    return relative


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
