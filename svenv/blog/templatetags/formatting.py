import dateutil.parser
from django import template
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
    return markdown2.markdown(value, extras=['fenced-code-blocks'])
