import jinja2

class TemplateEngine(object):
    def __init__(self, template_path):
        self.env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(template_path))

    def render(self, template, context):
        template = self.env.get_template(template)
        return template.render(context)
