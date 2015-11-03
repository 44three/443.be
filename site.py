from os import listdir, makedirs, path, walk

from jinja2 import Environment, FileSystemLoader
import mistune

from ext.mistune_contrib import HighlightMixin


BUILD_DIR = 'build/'
CONTENT_DIR = 'content/'
BLOG_CONTENT_DIR = path.join(CONTENT_DIR, 'blog/')
TEMPLATE_DIR = '_templates'


class Renderer(mistune.Renderer, HighlightMixin):
    pass


renderer = Renderer()
markdown = mistune.Markdown(renderer=renderer)
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def render_and_write(content, template):
    """ Render (.md|.html) content using the template provided """
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
    """ Build the pages for the site """

    pages = [
        page for page in listdir(CONTENT_DIR)
        if page.endswith(tuple(['.html', '.md']))
    ]

    for page in pages:
        render_and_write(page, env.get_template('page.html'))


def make_blog_posts():
    """ Build the blog posts

    Any .md or .html file in the BLOG_CONTENT_DIR will be rendered as 
    BLOG_CONTENT_DIR/path/to/page_name/index.html
    """

    posts = [
        path.relpath(path.join(root, filename), CONTENT_DIR)
        for root, dirnames, filenames in walk(BLOG_CONTENT_DIR)
        for filename in filenames if filename.endswith(tuple(['.html', '.md']))
    ]

    for post in posts:
        render_and_write(post, env.get_template('post.html'))


if __name__ == '__main__':
    makedirs(BUILD_DIR, exist_ok=True)
    make_pages()
    make_blog_posts()
