import copy
import uuid

from flask import jsonify, request, abort, Response, Blueprint, logging
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from github_interface.interface import GithubInterface
from mongo.credentials import CredentialsManager
from mongo.models import Document
from utils import code_formatter
from utils.constants import SECRET_PASSWORD_FORGERY, CLIENT_ID, CLIENT_SECRET, REDIRECT_URL_LOGIN
from utils.file_interface import FileInterface

web_server = Blueprint('web_server', __name__, )


@web_server.route("/repos")
def repos():
    # Get the repository list
    repo_names = [r.full_name for r in GithubInterface.get_repos()]

    # Return the response
    return __create_response(repo_names)


@web_server.route("/file")
def file():
    # Get the repository
    repo_name = request.args.get('repo')

    if not repo_name:
        return abort(400, "A repo should be specified")

    repo = GithubInterface.get_repo(repo_name)

    # Get the content at path
    path_arg = request.args.get('path')
    path = path_arg if path_arg else ""

    # TODO: fix this so we don't have to deepcopy
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
    return __create_response(repo_object)


@web_server.route("/save", methods=['POST', 'OPTIONS'])
def save():
    if request.method == 'OPTIONS':
        return __create_option_response()

    if Document.find(request.get_json().get('name')):
        return abort(400, 'Document name already exists')

    doc = Document.from_json(request.get_json())
    doc.insert()

    return __create_response({})


@web_server.route("/docs")
def docs():
    docs = Document.get_all()

    return __create_response([doc.to_json() for doc in docs])


@web_server.route("/render")
def render():
    name = request.args.get('name')

    # Get the documentation doc
    doc = Document.find(name)

    references = {}

    for ref in doc.references:
        repo = GithubInterface.get_repo(ref.repo)

        content = '\n'.join(repo.get_lines_at_path(ref.path, ref.start_line, ref.end_line))
        formatted_code = code_formatter.format(ref.path, content, ref.start_line)

        references[ref.ref_id] = {
            'code': formatted_code,
            'repo': ref.repo,
            'path': ref.path,
            'startLine': ref.start_line,
            'endLine': ref.end_line,
        }

    return __create_response({
        'name': name,
        'content': doc.content,
        'refs': references
    })


# TODO: similar to render -> refactor later
@web_server.route("/lines")
def get_lines():
    repo = request.args.get('repo')
    path = request.args.get('path')
    start_line = int(request.args.get('startLine'))
    end_line = int(request.args.get('endLine'))

    repository = GithubInterface.get_repo(repo)
    content = ''.join(repository.get_content_at_path(path).content.splitlines(keepends=True)[start_line - 1: end_line])

    try:
        lexer = get_lexer_for_filename(path)
    except ClassNotFound:
        lexer = TextLexer()  # use a generic lexer if we can't find anything

    formatter = HtmlFormatter(noclasses=True, linenos='table', linespans='code-line', linenostart=start_line)
    code = highlight(content, lexer, formatter)

    return __create_response({
        'ref_id': str(uuid.uuid1()),  # generate a unique id for the reference
        'code': code,
        'repo': repo,
        'path': path,
        'startLine': start_line,
        'endLine': end_line,
    })


@web_server.route("/auth/github/callback", methods=['POST', 'OPTIONS'])
def auth_github_callback():
    if request.method == 'OPTIONS':
        return __create_option_response()

    temporary_code = request.args.get('code')
    state = request.args.get('state')

    if state != SECRET_PASSWORD_FORGERY:
        abort(401)

    user_access_token = GithubInterface.get_user_access_token(CLIENT_ID, CLIENT_SECRET, temporary_code,
                                                              REDIRECT_URL_LOGIN)
    CredentialsManager.write_credentials(user_access_token=user_access_token)

    return __create_response({})


@web_server.route("/installs")
def installs():
    user_access_token = CredentialsManager.read_credentials()["user_access_token"]
    if not user_access_token:
        user_installations = {"installations": []}
    else:
        user_installations = GithubInterface.get_user_installations()

    return __create_response({
        "installations": user_installations["installations"]
    })


@web_server.route("/installs/installation_selection")
def installs_installation_selection():
    installation_id = request.args.get('installation_id')

    CredentialsManager.write_credentials(
        installation_access_token=GithubInterface.get_installation_access_token(installation_id,
                                                                                FileInterface.load_private_key()))

    return __create_response({})


@web_server.route("/github_app_installation_callback")
def github_app_installation_callback():
    """
    TODO: fix bug, when coming back from the installation page from github to the callback with my main account (saturnin13)
    the installation_id in the url is set to "undefined". find why and fix it.
    """
    installation_id = request.args.get('installation_id')
    setup_action = request.args.get('setup_action')

    installation_access_token = GithubInterface.get_installation_access_token(installation_id,
                                                                              FileInterface.load_private_key())

    CredentialsManager.write_credentials(installation_access_token=installation_access_token)

    installation = {}
    if CredentialsManager.read_credentials()["user_access_token"]:
        user_installations = GithubInterface.get_user_installations()

        for installation in user_installations["installations"]:
            if installation["id"] == installation_id:
                installation = installation

    return __create_response({
        "installation": installation
    })


def __create_response(json):
    return jsonify(json)


def __create_option_response():
    return Response()
