reSTsite Overview
=================

About
-----
  * A static site generator centering on reStructuredText.
  * Content split from presentation through the use of templates.
  * Uses:
      * [Docutils](http://docutils.sourceforge.net/) for reStructuredText parsing
      * [Pygments](http://pygments.org/) for syntax highlighting
      * [Jinja2](http://jinja.pocoo.org/2/) for templating
      * [PyYAML](http://pyyaml.org/) for configuration parsing
  * Inspired by [Jekyll](http://jekyllrb.com/) and [Hyde](http://ringce.com/hyde).
  * *Absolutely not stable or ready for production use!*

TODO
----
There are LOTS of things I still need to do, this list is mainly here to remind me:

  * Allow configuration of logging level in `_config.yaml`
  * Move `_templates` to `_layouts`
  * Allow configuration of which handlers are loaded
