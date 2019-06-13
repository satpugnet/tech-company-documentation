from flask import Flask, jsonify
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_for_filename

from github_interface.interface import GithubInterface

app = Flask(__name__)


@app.route("/github")
def github():
    g = GithubInterface("39180cc3f47072520e81a31484291ea5acc5af9f")
    repo = g.get_repo("saturnin13/tech-company-documentation")
    lines = repo.get_file("website/src/main.js").get_content()

    # Lexer to determine language
    lexer = get_lexer_for_filename("website/src/main.js")
    formatter = HtmlFormatter(noclasses=True, cssclass='card card-body')
    result = highlight(lines, lexer, formatter)

    result = '# This is awesome\n## This is also cool\n Here is some highlighted code using the library [pigments](http://pygments.org/docs/quickstart/)\n\n' \
             + result

    resp = jsonify(result)
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp


if __name__ == '__main__':
    app.run()