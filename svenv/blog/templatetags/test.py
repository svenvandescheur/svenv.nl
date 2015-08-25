from .formatting import svenv_flavored_markdown
from markdown2 import Markdown
from textwrap import dedent
from unittest import TestCase


class MarkdownTest(TestCase):
    """
    Tests svenv flavored markdown against specification found on: http://daringfireball.net/projects/markdown/basics
    Newlines are ignored
    """
    def setUp(self):
        self.md = Markdown(extras=['fenced-code-blocks'])
        self.mdf = svenv_flavored_markdown(extras=['fenced-code-blocks'])

    def test_paragraphs_headers_blockquotes(self):
        markdown = dedent(
            """
            A First Level Header
            ====================

            A Second Level Header
            ---------------------

            Now is the time for all good men to come to
            the aid of their country. This is just a
            regular paragraph.

            The quick brown fox jumped over the lazy
            dog's back.

            ### Header 3

            > This is a blockquote.
            >
            > This is the second paragraph in the blockquote.
            >
            > ## This is an H2 in a blockquote
            """
        )

        html = dedent(
            """
            <h1>A First Level Header</h1>

            <h2>A Second Level Header</h2>

            <p>Now is the time for all good men to come to
            the aid of their country. This is just a
            regular paragraph.</p>

            <p>The quick brown fox jumped over the lazy
            dog's back.</p>

            <h3>Header 3</h3>

            <blockquote>
              <p>This is a blockquote.</p>

              <p>This is the second paragraph in the blockquote.</p>

              <h2>This is an H2 in a blockquote</h2>
            </blockquote>
            """
        )
        self.assert_markdown(markdown, html)

    def test_phrase_emphasis(self):
        markdown = dedent(
            """
            Some of these words *are emphasized*.
            Some of these words _are emphasized also_.

            Use two asterisks for **strong emphasis**.
            Or, if you prefer, __use two underscores instead__.
            """
        )

        html = dedent(
            """
            <p>Some of these words <em>are emphasized</em>.
            Some of these words <em>are emphasized also</em>.</p>

            <p>Use two asterisks for <strong>strong emphasis</strong>.
            Or, if you prefer, <strong>use two underscores instead</strong>.</p>
            """
        )
        self.assert_markdown(markdown, html)

    def test_unordered_lists(self):
        asterisk = dedent(
            """
            *   Candy.
            *   Gum.
            *   Booze.
            """
        )

        plus = dedent(
            """
            +   Candy.
            +   Gum.
            +   Booze.
            """
        )

        hyphen = dedent(
            """
            -   Candy.
            -   Gum.
            -   Booze.
            """
        )

        html = dedent(
            """
            <ul>
            <li>Candy.</li>
            <li>Gum.</li>
            <li>Booze.</li>
            </ul>
            """
        )
        self.assert_markdown(asterisk, html, 'Asterisk style list did not parse correctly')
        self.assert_markdown(plus, html, 'Plus style list did not parse correctly')
        self.assert_markdown(hyphen, html, 'Hyphen style list did not parse correctly')

    def test_ordered_lists(self):
        """
        Svenv flavored markdown respects list start
        """
        markdown = dedent(
            """
            1.  Red
            2.  Green
            3.  Blue

            4.  Red
            5.  Green
            6.  Blue
            """
        )

        html = dedent(
            """
            <ol start="1">
            <li>Red</li>
            <li>Green</li>
            <li>Blue</li>
            </ol>
            <ol start="4">
            <li>Red</li>
            <li>Green</li>
            <li>Blue</li>
            </ol>
            """
        )
        self.assert_svenv_flavored_markdown(markdown, html)

    def test_paragraph_list(self):
        markdown = dedent(
            """
            *   A list item.

                With multiple paragraphs.

            *   Another item in the list.
            """
        )

        html = dedent(
            """
            <ul>
            <li><p>A list item.</p>
            <p>With multiple paragraphs.</p></li>
            <li><p>Another item in the list.</p></li>
            </ul>
            """
        )
        self.assert_markdown(markdown, html)

    def test_links_no_title(self):
        markdown = dedent(
            """
            This is an [example link](http://example.com/).
            """
        )

        html = dedent(
            """
            <p>This is an <a href="http://example.com/">
            example link</a>.</p>
            """
        )
        self.assert_markdown(markdown, html)

    def test_links_title(self):
        markdown = dedent(
            """
            This is an [example link](http://example.com/ "With a Title").
            """
        )

        html = dedent(
            """
            <p>This is an <a href="http://example.com/" title="With a Title">
            example link</a>.</p>
            """
        )
        self.assert_markdown(markdown, html)

    def test_reference_links(self):
        markdown = dedent(
            """
            I get 10 times more traffic from [Google][1] than from
            [Yahoo][2] or [MSN][3].

            [1]: http://google.com/        "Google"
            [2]: http://search.yahoo.com/  "Yahoo Search"
            [3]: http://search.msn.com/    "MSN Search"
            """
        )

        html = dedent(
            """
            <p>I get 10 times more traffic from <a href="http://google.com/"
            title="Google">Google</a> than from <a href="http://search.yahoo.com/"
            title="Yahoo Search">Yahoo</a> or <a href="http://search.msn.com/"
            title="MSN Search">MSN</a>.</p>
            """
        )
        self.assert_markdown(markdown, html)

    def test_images(self):
        """
        Paragraphs seem to be added by Markdown2
        """
        markdown = dedent(
            """
            ![alt text](/path/to/img.jpg "Title")
            """
        )

        html = dedent(
            """
            <p><img src="/path/to/img.jpg" alt="alt text" title="Title" /></p>
            """
        )
        self.assert_markdown(markdown, html)

    def test_code_backticks(self):
        markdown = dedent(
            """
            I strongly recommend against using any `<blink>` tags.

            I wish SmartyPants used named entities like `&mdash;`
            instead of decimal-encoded entites like `&#8212;`.
            """
        )

        html = dedent(
            """
            <p>I strongly recommend against using any
            <code>&lt;blink&gt;</code> tags.</p>

            <p>I wish SmartyPants used named entities like
            <code>&amp;mdash;</code> instead of decimal-encoded
            entites like <code>&amp;#8212;</code>.</p>
            """
        )
        self.assert_markdown(markdown, html)

    def test_code_indent(self):
        markdown = """
If you want your page to validate under XHTML 1.0 Strict,
you've got to put paragraph tags in your blockquotes:

    <blockquote>
        <p>For example.</p>
    </blockquote>
        """

        html = dedent(
            """
            <p>If you want your page to validate under XHTML 1.0 Strict,
            you've got to put paragraph tags in your blockquotes:</p>

            <pre><code>&lt;blockquote&gt;
                &lt;p&gt;For example.&lt;/p&gt;
            &lt;/blockquote&gt;
            </code></pre>
            """
        )
        self.assert_markdown(markdown, html)

    def test_fenched_code_blocks(self):
        """
        Basic test for the Markdown2 fenched code blocks extra
        """
        markdown = dedent(
            """
            ```
            some code
            ```
            """
        )

        html = dedent(
            """
            <pre><code>some code</code></pre>
            """
        )
        self.assert_markdown(markdown, html)

    def test_svenv_flavored_markdown(self):
        """
        Tests "svenv flavored" markdown
        """
        markdown = dedent(
            """
            ![alt text](/path/to/img.jpg "Title" "Class")
            """
        )

        html = dedent(
            """
             <p><img src="/path/to/img.jpg" alt="alt text" title="Title" class="Class" /></p>
            """
        )
        self.assert_svenv_flavored_markdown(markdown, html)

    def assert_markdown(self, markdown, html, msg=None):
        """
        Tests both markdown2 and "svenv flavored markdown"
        """
        self.assert_markdown2(markdown, html, msg)
        self.assert_svenv_flavored_markdown(markdown, html, msg)

    def assert_markdown2(self, markdown, html, msg=None):
        """
        Converts markdown and asserts against given html
        Newlines and spaces are ignored for test (so are in-text spaces)
        """
        result = self.md.convert(markdown)

        result = result.replace('\n', '')
        result = result.replace(' ', '')
        html = html.replace('\n', '')
        html = html.replace(' ', '')

        self.assertEqual(result, html, msg)

    def assert_svenv_flavored_markdown(self, markdown, html, msg=None):
        """
        Converts markdown and asserts against given html
        Newlines and spaces are ignored for test (so are in-text spaces)
        """
        result = self.mdf.convert(markdown)

        result = result.replace('\n', '')
        result = result.replace(' ', '')
        html = html.replace('\n', '')
        html = html.replace(' ', '')

        self.assertEqual(result, html, msg)