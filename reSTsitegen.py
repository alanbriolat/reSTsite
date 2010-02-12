import docutils.core
import reSTsite.rst

reSTsite.rst.register_directives()

docutils.core.publish_cmdline(writer_name='html')
