from itertools import groupby, islice, izip
import logging
_log = logging.getLogger('reSTsite.dir_processors')

from reSTsite.processor import Processor
from reSTsite.util import pairwise

import pprint
pp = pprint.PrettyPrinter(indent=4)


def date_chain(items):
    for a, b in pairwise(items):
        a['prev_by_date'] = b
        b['next_by_date'] = a
    items[0]['next_by_date'] = None
    items[-1]['prev_by_date'] = None


class ArchiveMonth(dict):
    def __init__(self, site, year, month, files):
        dict.__init__(self)
        self.site = site
        self['year'] = year
        self['month'] = month
        self['files'] = files
        self['title'] = 'Archive for %(year)s/%(month)s' % self

    @property
    def url(self):
        return self.site.url('%(year)s/%(month)s/' % self)

    @property
    def destpath(self):
        return '%(year)s/%(month)s/index.html' % self

    @property
    def abs_destpath(self):
        return self.site.abs_destpath(self.destpath)


class ArchiveYear(dict):
    def __init__(self, site, year, files):
        dict.__init__(self)
        self.site = site
        self['year'] = year
        self['files'] = files
        self['title'] = 'Archive for %(year)s' % self
        self['months'] = list()
        for month, files in groupby(files, key=lambda f: f['month']):
            self['months'].append(ArchiveMonth(self.site, year, month, list(files)))
        date_chain(self['months'])
        self['month_lookup'] = dict((m['month'], m) for m in self['months'])

    @property
    def url(self):
        return self.site.url('%(year)s' % self)

    @property
    def destpath(self):
        return '%(year)s/index.html' % self

    @property
    def abs_destpath(self):
        return self.site.abs_destpath(self.destpath)


class Archive(dict):
    def __init__(self, site, files):
        dict.__init__(self)
        self.site = site

        # Create list of files sorted by date
        self['files'] = sorted(files,
                               key=lambda f: '%(year)s%(month)s%(day)s' % f,
                               reverse=True)
        date_chain(self['files'])
        self['title'] = 'Archive'
        self['years'] = list()
        for year, files in groupby(self['files'], key=lambda f: f['year']):
            self['years'].append(ArchiveYear(site, year, list(files)))
        date_chain(self['years'])
        self['year_lookup'] = dict((y['year'], y) for y in self['years'])

        # Fix the month date chaining
        for a, b in pairwise(self['years']):
            a['months'][-1]['prev_by_date'] = b['months'][0]
            b['months'][0]['next_by_date'] = a['months'][-1]


class ArchiveProcessor(Processor):
    def __init__(self, tpl_year='archive.html', tpl_month='archive.html'):
        self.tpl_year = tpl_year
        self.tpl_month = tpl_month

    def process(self, d):
        d['archive'] = Archive(d.site, d.files)

    def generate(self, d):
        for y in d['archive']['years']:
            for m in y['months']:
                _log.debug('Generating archive file ' + m.destpath)
                d.site.tpl.render_layout_to_path(self.tpl_month,
                                                 m.abs_destpath,
                                                 {'this': m})
            _log.debug('Generating archive file ' + y.destpath)
            d.site.tpl.render_layout_to_path(self.tpl_year,
                                             y.abs_destpath,
                                             {'this': y})
