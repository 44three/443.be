from os import listdir, makedirs, path, walk
from jinja2 import Environment, FileSystemLoader

import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

BUILD_DIR = 'build/'
CONTENT_DIR = 'content/'
BLOG_CONTENT_DIR = path.join(CONTENT_DIR, 'blog/')


class HighlightRenderer(mistune.Renderer):

    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)


renderer = HighlightRenderer()
markdown = mistune.Markdown(renderer=renderer)
env = Environment(loader= FileSystemLoader('_templates'))

t_page = env.get_template('page.html')
t_post = env.get_template('post.html')


def render_and_write(content, template):
    with open(path.join(CONTENT_DIR, content), 'r') as f:
        html = markdown(f.read())

    _path, _ = path.splitext(content)
    if not _path.endswith('index'):
        makedirs(path.join(BUILD_DIR, _path), exist_ok=True)
        out_path = path.join(BUILD_DIR, _path, 'index.html')
    else:
        out_path = path.join(BUILD_DIR, 'index.html')

    with open(out_path, 'w') as f:
        f.write(template.render(content=html))


def make_pages():
    """ Build the pages for the site

    Any .html or .md file in the CONTENT_DIR will be rendered as 
    BUILD_DIR/page_name/index.html
    """

    pages = [
        page for page in listdir(CONTENT_DIR)
        if page.endswith(tuple(['.html', '.md']))
    ]

    for page in pages:
        render_and_write(page, t_page)


def make_blog_posts():
    """ Build the blog posts

    Any .md or .html file in the BLOG_CONTENT_DIR will be rendered as 
    BUILD_DIR/page_name/index.html
    """

    posts = [
        path.relpath(path.join(root, filename), CONTENT_DIR)
        for root, dirnames, filenames in walk(BLOG_CONTENT_DIR)
        for filename in filenames if filename.endswith(tuple(['.html', '.md']))
    ]

    for post in posts:
        render_and_write(post, t_post)


if __name__ == '__main__':
    makedirs(BUILD_DIR, exist_ok=True)
    make_pages()
    make_blog_posts()
