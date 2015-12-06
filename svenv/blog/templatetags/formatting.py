import dateutil.parser
from django import template
from re import finditer, search, sub, match, MULTILINE
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

    def _do_lists(self, text):
        """
        Replace the markdown2 _do_lists function
        Uses the same syntax but respects user's list start
        """
        matches = finditer(r'(\d+\.\s+?.+\n|\r)+', text, MULTILINE)

        for m in matches:
            list = m.group(0)
            list = match('\d+?\.[^<]+', list).group(0)
            text = text.replace(list, self.parse_markdown_sane_list(list))

        return super(svenv_flavored_markdown, self)._do_lists(text)

    def parse_markdown_sane_list(self, list):
        """
        Find the first item in the lists and uses it as start
        Returns the html version of the list
        """
        lines = list.splitlines()
        match_start = search(r'(\d+)\.', lines[0])
        start = match_start.group(1)
        html = '<ol start="' + start + '">'

        for line in lines:
            match_content = search(r'\d+\.\s(.+)', line)
            html += '<li>' + match_content.group(1) + '</li>'
        html += '</ol>'

        return html