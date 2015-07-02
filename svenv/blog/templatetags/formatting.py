import dateutil.parser
from django import template
from re import sub
import markdown2


register = template.Library()

@register.filter
def datetime(value):
    try:
        return dateutil.parser.parse(value)
    except(AttributeError):
        return value


@register.filter
def markdown(value):
    value = markdown_class_image(value)
    return markdown2.markdown(value, extras=['fenced-code-blocks'])


def markdown_class_image(value):
    """
    Extends markdown image syntax with additional class parameter
    """
    value = sub(r'!\[(.+?)]\((.+?)\s+["\'](.+)["\']\s["\'](.+?)["\']\)',
                  r'<img alt="\1" src="\2" title="\3" class="\4" />', value)
    return value