import copy

from flask import Flask, jsonify, request, abort, Response
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from github_interface.interface import GithubInterface
from mongo.models import Document
from utils.json.custom_json_encoder import CustomJsonEncoder

app = Flask(__name__)

app.json_encoder = CustomJsonEncoder

github_interface = GithubInterface("39180cc3f47072520e81a31484291ea5acc5af9f")

@app.route("/github")
def github():
    repo = github_interface.get_repo("saturnin13/tech-company-documentation")
    content = repo.get_content_at_path("website/src/main.js").content

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
    # Get the repository list
    repo_names = [r.full_name for r in github_interface.get_repos()]

    # Return the response
    response = jsonify(repo_names)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


@app.route("/file")
def files():
    # Get the repository
    repo_name = request.args.get('repo')

    if not repo_name:
        return abort(400, "A repo should be specified")

    # repo = g.get_repo("saturnin13/tech-company-documentation")
    repo = github_interface.get_repo(repo_name)

    # Get the content at path
    path_arg = request.args.get('path')
    path = path_arg if path_arg else ""

    repo_object = copy.deepcopy(repo.get_content_at_path(path))

    # Syntax highlighting for file
    if repo_object.type == 'file':
        try:
            lexer = get_lexer_for_filename(path)
        except ClassNotFound:
            lexer = TextLexer()  # use a generic lexer if we can't find anything

        formatter = HtmlFormatter(noclasses=True, linenos='table', linespans='code-line')
        repo_object.content = highlight(repo_object.content, lexer, formatter)

    # Return the response
    response = jsonify(repo_object)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


@app.route("/save", methods=['POST', 'OPTIONS'])
def save():
    if request.method == 'OPTIONS':
        response = Response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    if Document.find(request.get_json().get('name')):
        return abort(400, 'Document name already exists')

    doc = Document.from_json(request.get_json())
    doc.insert()

    response = Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/docs")
def docs():
    docs = Document.get_all()

    response = jsonify([doc.to_json() for doc in docs])
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/render")
def render():
    name = request.args.get('name')
    doc = Document.find(name)

    ref = doc.references[0]

    repo = github_interface.get_repo(ref.repo)
    content = ''.join(repo.get_content_at_path(ref.path).content.splitlines(keepends=True)[ref.start_line-1: ref.end_line])

    try:
        lexer = get_lexer_for_filename(ref.path)
    except ClassNotFound:
        lexer = TextLexer()  # use a generic lexer if we can't find anything

    formatter = HtmlFormatter(noclasses=True, linenos='table', linespans='code-line', linenostart=ref.start_line)
    code = highlight(content, lexer, formatter)

    response = jsonify({
        'name': name,
        'content': doc.content,
        'code': code
    })

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run()