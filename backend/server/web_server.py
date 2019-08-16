import copy
import logging
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
from mongo.models.db_document import DbDocument
from mongo.models.db_account_installation import DbAccountInstallation
from mongo.models.db_user import DbUser
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
        if not __is_user_authorised():
            return __create_unauthorised_response()
        return f(*args, **kwargs)

    return wrap

def org_user_access_validation_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not __can_user_access_org_user_account():
            return __create_unauthorised_response()
        return f(*args, **kwargs)

    return wrap


@web_server.route("/logout")
@login_required
def logout():
    session.pop('user_login')
    return __create_response({})

@web_server.route("/<path:org_user_account>/repos")
@login_required
@org_user_access_validation_required
def repos(org_user_account):
    # Get the repository list

    repo_names = [r.full_name for r in AuthenticatedGithubInterface(session['user_login']).get_repos(org_user_account)]

    # Return the response
    return __create_response(repo_names)


@web_server.route("/<path:org_user_account>/file")
@login_required
@org_user_access_validation_required
def file(org_user_account):
    # Get the repository
    repo_name = request.args.get('repo')

    if not repo_name:
        return abort(400, "A repo should be specified")

    repo = AuthenticatedGithubInterface(session['user_login']).get_repo(org_user_account, repo_name)

    # Get the content at path
    path_arg = request.args.get('path')
    path = path_arg if path_arg else ""

    # TODO: fix this so we don't have to deepcopy
    fs_node = copy.deepcopy(repo.get_content_at_path(path))

    # Syntax highlighting for file
    if fs_node.type == 'file':
        try:
            lexer = get_lexer_for_filename(path)
        except ClassNotFound:
            lexer = TextLexer()  # use a generic lexer if we can't find anything

        formatter = HtmlFormatter(noclasses=True, linenos='table', linespans='code-line')
        fs_node.content = highlight(fs_node.content, lexer, formatter)

    # Return the response
    # TODO: return only the necessary fields, not the entire repo object
    return __create_response(fs_node)


@web_server.route("/<path:org_user_account>/save", methods=['POST', 'OPTIONS'])
@login_required
@org_user_access_validation_required
def save(org_user_account):
    if DbDocument.find(org_user_account, request.get_json().get('name')):
        return abort(400, 'Document name already exists')

    new_doc = request.get_json()
    new_doc["org_user_account"] = org_user_account

    doc = DbDocument.from_json(new_doc)
    doc.insert()

    return __create_response({})

@web_server.route("/<path:org_user_account>/docs")
@login_required
@org_user_access_validation_required
def docs(org_user_account):
    docs = DbDocument.get_all(org_user_account)

    return __create_response([doc.to_json() for doc in docs])

@web_server.route("/<path:org_user_account>/render")
@login_required
@org_user_access_validation_required
def render(org_user_account):
    name = request.args.get('name')

    # Get the documentation doc
    doc = DbDocument.find(org_user_account, name)

    references = {}

    for ref in doc.references:
        repo = AuthenticatedGithubInterface(session['user_login']).get_repo(org_user_account, ref.repo)

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
@web_server.route("/<path:org_user_account>/lines")
@login_required
@org_user_access_validation_required
def get_lines(org_user_account):
    repo = request.args.get('repo')
    path = request.args.get('path')
    start_line = int(request.args.get('startLine'))
    end_line = int(request.args.get('endLine'))

    repository = AuthenticatedGithubInterface(session['user_login']).get_repo(org_user_account, repo)
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

    user_token = GithubAuthorisationInterface.get_user_token(CLIENT_ID, CLIENT_SECRET, temporary_code, REDIRECT_URL_LOGIN)

    session['user_login'] = NonAuthenticatedGithubInterface.get_user_login(user_token)
    DbUser.upsert_user_token(session['user_login'], user_token)

    return __create_response({})


@web_server.route("/installs", methods=['POST', 'OPTIONS'])
@login_required
def installs():
    logging.critical('This is a debug message')
    user_installations = AuthenticatedGithubInterface(session['user_login']).get_user_installations()

    returned_installation = []
    for installation in user_installations:
        # TODO: delete the use of insert_if_not_exist here if it is now setup using the webhook
        DbAccountInstallation.insert_if_not_exist(installation.account["login"], installation.id)
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


def __is_user_authorised():
    authorised = 'user_login' in session
    if not authorised:
        print("User not authorised for {}".format(request.path))
    return authorised

def __can_user_access_org_user_account():
    user_installations = AuthenticatedGithubInterface(session['user_login']).get_user_installations()
    user = request.path.split('/')[2]

    for installation in user_installations:
        if user == installation.account["login"]:
            return True

    print('User {} is not authorised to access this installation for {}'.format(user, request.path))
    return False


def __create_unauthorised_response():
    return abort(403)  # Forbidden to access the resource


def __create_response(json):
    return jsonify(json)


def __create_option_response():
    return Response()
