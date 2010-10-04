from reSTsite.processor import Processor


class Jinja2Output(Processor):
    def __init__(self, template, extension='.html'):
        self.template = template
        self.extension = extension

    def process(self, f):
        f['template'] = self.template
        f.change_extension(self.extension)

    def generate(self, f):
        f.open_dest()
        context = f.to_context()
        template = f.site.tpl.get_template('layout/' + f['template'])
        template.stream(context).dump(f.abs_destpath)


class Jinja2Metadata(Processor):
    def process(self, f):
        f.update(f.site.tpl.get_metadata(f.sourcepath))


class Jinja2Processor(Processor):
    def generate(self, f):
        f.open_dest()
        context = f.to_context()
        template = f.site.tpl.get_template('site/' + f.sourcepath)
        template.stream(context).dump(f.abs_destpath)
