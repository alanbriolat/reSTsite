import jinja2

class TemplateEngine(object):
    """
    A simple wrapper around Jinja2 templating to provide the functionality
    needed by reSTsite
    """
    def __init__(self, template_path):
        """
        Create the Jinja2 enironment
        """
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))

    def render(self, template, context):
        """
        Render the given template with the given context
        """
        template = self.env.get_template(template)
        return template.render(context)
