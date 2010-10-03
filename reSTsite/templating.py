import os.path

from jinja2 import Environment, FileSystemLoader, PrefixLoader


class reSTsiteEnvironment(Environment):
    def __init__(self, site):
        options = {}
        options['loader'] = PrefixLoader({
            'layout': FileSystemLoader(os.path.join(site.options.site_path,
                                                    site.settings.TEMPLATE_DIR)),
            'site': FileSystemLoader(site.options.site_path),
        })

        Environment.__init__(self, **options)

    def join_path(self, template, parent):
        """Restrict templated files to only opening other layout templates."""
        return 'layout/' + template

    def get_metadata(self, template):
        template = self.get_template('site/' + template)
        if hasattr(template.module, 'metadata'):
            return template.module.metadata.copy()
        else:
            return dict()
