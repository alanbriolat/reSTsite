import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('reSTsite')
import shutil
import os.path

import reSTsite.handlers
import reSTsite.filesystem as fs

reSTsite.handlers.load_handlers(('Jinja', ))
handlers = reSTsite.handlers.get_extension_handlers()

SITE_DIR = 'content'
STATIC_DIR = 'static'
DEPLOY_DIR = 'deploy'

# Walk files to be copied
for full, rel, ext in fs.walk(STATIC_DIR):
    log.info('Copying static %s' % rel)
    fs.copy(full, os.path.join(DEPLOY_DIR, rel))

# Walk files to be processed
for full, rel, ext in fs.walk(SITE_DIR):
    # Skip unhandled extensions
    if ext in handlers:
        log.info('Processing %s' % rel)
        source = full
        dest = os.path.splitext(os.path.join(DEPLOY_DIR, rel))[0]

        handler = handlers[ext]()
        fs.create(dest).write(handler.render_from_file(source))
