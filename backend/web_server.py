from flask import Flask, jsonify, request, abort
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from github_interface import interface

app = Flask(__name__)


@app.route("/github")
def github():
    g = interface.GithubInterface("39180cc3f47072520e81a31484291ea5acc5af9f")
    repo = g.get_repo("saturnin13/tech-company-documentation")
    content = repo.get_content_at_path("website/src/main.js").get('content')

    # Lexer to determine language
    lexer = get_lexer_for_filename("website/src/main.js")
    formatter = HtmlFormatter(noclasses=True, cssclass='card card-body')
    result = highlight(content, lexer, formatter)

    result = '# This is awesome\n## This is also cool\n Here is some highlighted code using the library [pigments](http://pygments.org/docs/quickstart/)\n\n' \
             + result

    response = jsonify(result)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


@app.route("/repos")
def repos():
    g = interface.GithubInterface("39180cc3f47072520e81a31484291ea5acc5af9f")

    # Get the repository list
    repo_names = g.get_repo_names()

    # Return the response
    response = jsonify(repo_names)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


@app.route("/file")
def files():
    g = interface.GithubInterface("39180cc3f47072520e81a31484291ea5acc5af9f")

    # Get the repository
    repo_name = request.args.get('repo')

    if not repo_name:
        return abort(400, "A repo should be specified")

    # repo = g.get_repo("saturnin13/tech-company-documentation")
    repo = g.get_repo(repo_name)

    # Get the content at path
    path_arg = request.args.get('path')
    path = path_arg if path_arg else ""

    content = repo.get_content_at_path(path)

    # Syntax highlighting for file
    if content['type'] == 'file':
        try:
            lexer = get_lexer_for_filename(path)
        except ClassNotFound:
            lexer = TextLexer()  # use a generic lexer if we can't find anything

        formatter = HtmlFormatter(noclasses=True, linenos='table', linespans='code-line')
        content['content'] = highlight(content['content'], lexer, formatter)

    # Return the response
    response = jsonify(content)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


if __name__ == '__main__':
    app.run()