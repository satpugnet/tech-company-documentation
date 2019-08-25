from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound


class CodeFormatter:
    """
    Formatting of code using a lexer.
    """

    def format(self, path, code, start_line=1):
        try:
            lexer = get_lexer_for_filename(path)

        except ClassNotFound:
            lexer = TextLexer()  # use a generic lexer if we can't find anything

        formatter = HtmlFormatter(noclasses=True, linenos='table', linespans='code-line', linenostart=start_line)

        return highlight(code, lexer, formatter)
