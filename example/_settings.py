import os.path

DEPLOY_DIR = '_deploy'
SITE_URL = '/~alan/reSTsite-example/'
#SITE_URL = 'file://' + os.path.abspath(os.path.join(os.path.dirname(__file__),
#                                                    DEPLOY_DIR))  + '/'

# Site content definitions
#
# CONTENT is a list of (basedir, options) pairs.  The contents of basedir are
# processed and put into DEPLOY_DIR, preserving path (excluding basedir) unless
# a processor modifies the target path.  basedirs are processed in the order
# they are defined here.  If a basedir is a subdirectory of another basedir,
# it should probably be excluded by the first definition, i.e. hidden by an
# "exclude" pattern or the first definition being non-recursive.  Also be
# aware that files generated from later basedirs can overwrite those generated
# from earlier ones.

CONTENT = {
    '_': {
        'path': '',
        'file_processors': (
            ('*.rst', (
                'reSTsite.file_processors.RestructuredText',
                ('reSTsite.file_processors.Jinja2Output', {
                    'template': 'default.html',
                }),
            )),
            ('*.html', (
                'reSTsite.file_processors.Jinja2Metadata',
                'reSTsite.file_processors.Jinja2Processor',
            )),
        ),
    },
    'static': {
        'path': '_static',
        'file_processors': (
            ('*', (
                'reSTsite.file_processors.PassthroughProcessor',
            )),
        ),
    },
    'blog': {
        'path': '_blog',
        'file_processors': (
            ('*.rst', (
                'reSTsite.file_processors.PathMetadata',
                ('reSTsite.file_processors.RewriteTarget', {
                    'pattern': '%(year)s/%(month)s/%(slug)s%(ext)s',
                }),
                'reSTsite.file_processors.RestructuredText',
                ('reSTsite.file_processors.Jinja2Output', {
                    'template': 'blog.html',
                }),
            )),
        ),
        'dir_processors': (
            'reSTsite.dir_processors.ArchiveProcessor',
        ),
    },
}

# Method of running:
#
#   * For each directory in CONTENT:
#       * Convert exclude + include to "visible" function
#       * Convert file (pattern, processor, kwargs) to (pattern, processor) by creating processors
#       * Convert dir (processor, kwargs) to processor by creating processors
#       * For each file path under the directory discovered by walking the tree, taking into
#         account visibility and recursive setting:
#           * Create a file instance for the path
#           * Run each matching file_processor on the file, in order
#       * Run each dir_processor in order
#   * For each processed directory:
#       * Run .generate() on each file
#       * Run .generate() on the directory (e.g. for index processors, etc.)
#
# This allows metadata to be obtained first, and then used in generating output for files,
# so that it's possible to refer to other parts of the site, generate indexes, etc.
#
#
# An idea: cache the file data between process() and generate(), so that it can be loaded if the
# file hasn't changed since it was generated.  Need to possibly implement some of the pickle
# protocol to allow File objects to be pickled?
#

STYLESHEETS = (
    'css/pygments.css',
)
