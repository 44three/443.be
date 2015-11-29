# Start from Scratch

It only takes a few ingredients to create a blog from scratch.  All you really
need is some `html` and `css`. This blog is created with:

- [jinja2](http://jinja.pocoo.org/docs/dev/) for quick, easy, and robust `html`
  templates.
- [skeleton](http://getskeleton.com/) css for a "dead simple" responsive grid
  and more style than I know what to do with.
- [mistune](https://mistune.readthedocs.org/) for markdown processing because
  no one wants to write blog posts in html.
- [pygments](http://pygments.org/) for tasteful syntax highlighting in just
  about any language desired.

These amazing packages are utilized by a very short and simple python script
that:

- collects content files on the file system,
- converts markdown to html while applying syntax highlighting,
- injects html content into standard template pages, and
- writes the output to a build directory.

That's all.
