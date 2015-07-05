import dateutil.parser
from django import template
from re import sub, findall
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
    value = markdown2.markdown(value, extras=['fenced-code-blocks'])
    value = markdown_class_image(value)
    return value


def markdown_class_image(value):
    """
    Extends markdown image syntax with additional class parameter
    Syntax: ![Alt text](/path/to/img.jpg "Title" "Class")
    Replacement is ignored within <code> and <pre>
    """
    return sub(r'([\s\S]+?)!\[(.+?)]\((.+?)\s+["\'](.+)["\']\s["\'](.+?)["\']\)',
                  parse_markdown_class_image, value)


def parse_markdown_class_image(match):
    """
    Replaces the match with correct image tag if necessary
    If the match is fenched in either a <code>, or <pre> block it should be left intact
    """
    if is_fenched_in_block('code', match) or is_fenched_in_block('pre', match):
        return match.group(0)
    return r'<img alt="\2" src="\3" title="\4" class="\5" />'


def is_fenched_in_block(tag, match):
    """
    Compares number of tag starts with number of tag ends
    Returns True if number of tag starts is greater than number of tag ends
    """
    code_starts = findall(r'<'+tag, match.group(1))
    code_ends = findall(r'<\/'+tag, match.group(1))

    return len(code_starts) > len(code_ends)