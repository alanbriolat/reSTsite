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


class Jinja2Processor(Processor):
    def process(self, f):
        metadata = f.site.tpl.get_metadata(f.sourcepath)
        f.update(metadata)

    def generate(self, f):
        f.open_dest()
        context = f.to_context()
        template = f.site.tpl.get_template('site/' + f.sourcepath)
        template.stream(context).dump(f.abs_destpath)
