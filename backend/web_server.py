import copy
import uuid

from flask import Flask, jsonify, request, abort, Response
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from github_interface.interface import GithubInterface
from mongo.models import Document
from utils import code_formatter
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

    # Get the documentation doc
    doc = Document.find(name)

    references = {}

    for ref in doc.references:
        repo = github_interface.get_repo(ref.repo)

        content = '\n'.join(repo.get_lines_at_path(ref.path, ref.start_line, ref.end_line))
        formatted_code = code_formatter.format(ref.path, content, ref.start_line)

        references[ref.ref_id] = {
            'code': formatted_code,
            'repo': ref.repo,
            'path': ref.path,
            'startLine': ref.start_line,
            'endLine': ref.end_line,
        }

    response = jsonify({
        'name': name,
        'content': doc.content,
        'refs': references
    })

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# TODO: similar to render -> refactor later
@app.route("/lines")
def get_lines():
    repo = request.args.get('repo')
    path = request.args.get('path')
    start_line = int(request.args.get('startLine'))
    end_line = int(request.args.get('endLine'))

    repository = github_interface.get_repo(repo)
    content = ''.join(repository.get_content_at_path(path).content.splitlines(keepends=True)[start_line - 1: end_line])

    try:
        lexer = get_lexer_for_filename(path)
    except ClassNotFound:
        lexer = TextLexer()  # use a generic lexer if we can't find anything

    formatter = HtmlFormatter(noclasses=True, linenos='table', linespans='code-line', linenostart=start_line)
    code = highlight(content, lexer, formatter)

    response = jsonify({
        'ref': str(uuid.uuid1()),  # generate a unique id for the reference
        'content': {
            'code': code,
            'repo': repo,
            'path': path,
            'startLine': start_line,
            'endLine': end_line,
        }
    })

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run()