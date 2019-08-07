import copy
import uuid
from functools import wraps

from flask import jsonify, request, abort, Response, Blueprint, session
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from github_interface.authenticated_github_interface import AuthenticatedGithubInterface
from github_interface.authorisation_interface import GithubAuthorisationInterface
from github_interface.non_authenticated_github_interface import NonAuthenticatedGithubInterface
from mongo.models.document import Document
from mongo.models.installation import Installation
from mongo.models.user import User
from utils import code_formatter
from utils.constants import SECRET_PASSWORD_FORGERY, CLIENT_ID, CLIENT_SECRET, REDIRECT_URL_LOGIN

web_server = Blueprint('web_server', __name__)

@web_server.before_request
def before_request_func():
    if request.method == 'OPTIONS':
        return __create_option_response()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not __isUserAuthorised():
            print("User not authorised")
            return __create_unauthorised_response()
        return f(*args, **kwargs)

    return wrap

def installation_validation_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not __canUserAccessInstallation():
            print("User is not authorised to access this installation")
            return __create_unauthorised_response()
        return f(*args, **kwargs)

    return wrap

@web_server.route("/logout")
@login_required
def logout():
    session.pop('user_login')
    return __create_response({})

@web_server.route("/<path:installation_account_login>/repos")
@login_required
@installation_validation_required
def repos(installation_account_login):
    # Get the repository list
    repo_names = [r.full_name for r in AuthenticatedGithubInterface(session['user_login']).get_repos(installation_account_login)]

    # Return the response
    return __create_response(repo_names)

@web_server.route("/<path:installation_account_login>/file")
@login_required
@installation_validation_required
def file(installation_account_login):
    # Get the repository
    repo_name = request.args.get('repo')

    if not repo_name:
        return abort(400, "A repo should be specified")


    repo = AuthenticatedGithubInterface(session['user_login']).get_repo(installation_account_login, repo_name)

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
    # TODO: return only the necessary fields, not the entire repo object
    return __create_response(repo_object)


@web_server.route("/<path:installation_account_login>/save", methods=['POST', 'OPTIONS'])
@login_required
@installation_validation_required
def save(installation_account_login):
    if Document.find(installation_account_login, request.get_json().get('name')):
        return abort(400, 'Document name already exists')

    new_doc = request.get_json()
    new_doc["organisation"] = installation_account_login

    doc = Document.from_json(new_doc)
    doc.insert()

    return __create_response({})

@web_server.route("/<path:installation_account_login>/docs")
@login_required
@installation_validation_required
def docs(installation_account_login):
    docs = Document.get_all(installation_account_login)

    return __create_response([doc.to_json() for doc in docs])

@web_server.route("/<path:installation_account_login>/render")
@login_required
@installation_validation_required
def render(installation_account_login):
    name = request.args.get('name')

    # Get the documentation doc
    doc = Document.find(installation_account_login, name)

    references = {}

    for ref in doc.references:
        repo = AuthenticatedGithubInterface(session['user_login']).get_repo(installation_account_login, ref.repo)

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
@web_server.route("/<path:installation_account_login>/lines")
@login_required
@installation_validation_required
def get_lines(installation_account_login):
    repo = request.args.get('repo')
    path = request.args.get('path')
    start_line = int(request.args.get('startLine'))
    end_line = int(request.args.get('endLine'))

    repository = AuthenticatedGithubInterface(session['user_login']).get_repo(installation_account_login, repo)
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
    temporary_code = request.args.get('code')
    state = request.args.get('state')

    if state != SECRET_PASSWORD_FORGERY:
        abort(401)

    user_access_token = GithubAuthorisationInterface.get_user_access_token(CLIENT_ID, CLIENT_SECRET, temporary_code, REDIRECT_URL_LOGIN)

    session['user_login'] = NonAuthenticatedGithubInterface.get_user_login(user_access_token)
    User.upsert_user_token(session['user_login'], user_access_token)

    return __create_response({})

@web_server.route("/installs", methods=['POST', 'OPTIONS'])
@login_required
def installs():
    user_installations = AuthenticatedGithubInterface(session['user_login']).get_user_installations()

    returned_installation = []
    for installation in user_installations:
        Installation.insert_if_not_exist(installation.account["login"], installation.id)
        returned_installation.append(installation.to_json())

    return __create_response({
        "installations": returned_installation
    })

@web_server.route("/github_app_installation_callback", methods=['POST', 'OPTIONS'])
@login_required
def github_app_installation_callback():
    installation_id = request.args.get('installation_id')
    setup_action = request.args.get('setup_action')

    installation = {}
    user_installations = AuthenticatedGithubInterface(session['user_login']).get_user_installations()
    for user_installation in user_installations:
        if int(user_installation.id) == int(installation_id):
            installation = user_installation

    return __create_response({
        "login": installation.account["login"]
    })

@web_server.route("/user")
@login_required
def api_user():
    user_login = session['user_login']

    return __create_response({
        "user_login": user_login
    })


def __isUserAuthorised():
    return 'user_login' in session

def __canUserAccessInstallation():
    user_installations = AuthenticatedGithubInterface(session['user_login']).get_user_installations()

    for installation in user_installations:
        if request.path.split('/')[2] == installation.account["login"]:
            return True
    return False

def __create_unauthorised_response():
    return Response()

def __create_response(json):
    return jsonify(json)

def __create_option_response():
    return Response()
