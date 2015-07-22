import dateutil.parser
from django import template
from re import sub, findall
from markdown2 import Markdown


register = template.Library()


@register.filter
def datetime(value):
    try:
        return dateutil.parser.parse(value)
    except(AttributeError):
        return value


@register.filter
def markdown(value):
    """
    Runs "svenv flavored markdown" on value
    """
    md = svenv_flavored_markdown(extras=['fenced-code-blocks'])
    return md.convert(value)


class svenv_flavored_markdown(Markdown):
    def _do_links(self, value):
        """
        Extends markdown image syntax with additional class parameter
        Syntax: ![Alt text](/path/to/img.jpg "Title" "Class")
        """
        value = sub(r'!\[(.+?)]\((.+?)\s+?["\'](.+?)["\']\s*?(?:["\'](.+?)["\'])?\)',
                    self.parse_markdown_class_image, value)

        return super(svenv_flavored_markdown, self)._do_links(value)

    def parse_markdown_class_image(self, match):
        """
        Replaces the match with correct image tag
        """
        alt = match.group(1)
        src = match.group(2)
        title = match.group(3)
        classname = match.group(4)

        if classname is not None:
            html = '<img src="%s" alt="%s" title="%s" class="%s" />' % (src, alt, title, classname)
        else:
            html = '<img src="%s" alt="%s" title="%s" />' % (src, alt, title)

        return self._escape_special_chars(html)