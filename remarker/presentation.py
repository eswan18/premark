from jinja2 import Template

DEFAULT_JAVASCRIPT = """
<script src="https://remarkjs.com/downloads/remark-latest.min.js"></script>
<script>var slideshow = remark.create({ratio: '16:9', slideNumberFormat: '(%current%/%total%)', countIncrementalSlides: false, highlightLines: true});</script>"""

def generate_html(template_html, slide_markdown, stylesheet_html, title=None):
    """ Generate HTML for a Reveal.js presentation given a template_html,
    slide_markdown contents, and stylesheet_html. """

    # only support inline css for now, maybe links in the future
    stylesheet_html = '<style>\n{0}</style'.format(stylesheet_html)
    presentation = {
            'stylesheet_html': stylesheet_html,
            'slide_source': slide_markdown,
            'title': title,
            }
    remark = {
            'javascript': DEFAULT_JAVASCRIPT,
            }
    template = Template(template_html)
    return template.render(presentation=presentation, remark=remark)
