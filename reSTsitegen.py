import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('reSTsite')
import os.path

import reSTsite.handlers
import reSTsite.filesystem as fs


DEFAULTS = {
        # Global settings
        'site_path':        'content',
        'static_path':      'static',
        'deploy_path':      'deploy',
        'template_path':    'templates',
        'handlers':         ['reST'],
        # Per-content settings
        'title':            'Untitled',
        'template':         'default.html',
        }

SETTINGS = DEFAULTS

reSTsite.handlers.load_handlers(SETTINGS['handlers'])
handlers = reSTsite.handlers.get_extension_handlers()

from reSTsite.templates import TemplateEngine
tpl = TemplateEngine(SETTINGS['template_path'])

# Walk files to be copied
for full, rel, ext in fs.walk(SETTINGS['static_path']):
    log.info('Copying static %s' % rel)
    fs.copy(full, os.path.join(SETTINGS['deploy_path'], rel))

# Walk files to be processed
for full, rel, ext in fs.walk(SETTINGS['site_path']):
    # Skip unhandled extensions
    if ext in handlers:
        log.info('Processing %s' % rel)
        handler = handlers[ext]()
        dest = os.path.join(SETTINGS['deploy_path'], handler.translate_path(rel))
        metadata, context = handler.render_from_file(full, rel)
        context['metadata'] = metadata
        data = tpl.render(metadata.get('template', SETTINGS['template']), context)
        open(dest, 'w').write(data)
