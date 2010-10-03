import os.path

from jinja2 import Environment, FileSystemLoader, PrefixLoader


class reSTsiteEnvironment(Environment):
    """A customised Jinja2 template environment.

    Customises a Jinja2 environment to provide 2 template prefix paths: ``site/``
    corresponding to *site_path*, and ``layout/`` corresponding to
    *templates_path*.  :meth:`join_path` is overridden such that all template
    references from within other templates are to those in *templates_path*.
    """
    def __init__(self, site_path, templates_path, global_context):
        options = {}
        options['loader'] = PrefixLoader({
            'site': FileSystemLoader(site_path),
            'layout': FileSystemLoader(templates_path),
        })

        Environment.__init__(self, **options)
        self.globals.update(global_context)

    def join_path(self, template, parent):
        """Restrict templated files to only opening other layout templates."""
        return 'layout/' + template

    def get_metadata(self, template):
        """Get metadata variable from a template.

        Templated HTML source files should use ``{% set metadata = {...} %}``
        to set extra metadata for the document.  This method will load the
        *template* and return a copy of it's metadata, or an empty dict if none
        is present.
        """
        template = self.get_template('site/' + template)
        if hasattr(template.module, 'metadata'):
            return template.module.metadata.copy()
        else:
            return dict()

    def render_layout_to_path(self, template, path, context=None):
        template = self.get_template('layout/' + template)
        template.stream(context).dump(path)
