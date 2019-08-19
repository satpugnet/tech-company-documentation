import copy
import uuid
from functools import wraps

from flask import jsonify, request, abort, Response, Blueprint, session
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from github_interface.interfaces.authenticated_github_interface import AuthenticatedGithubInterface
from github_interface.interfaces.github_authorisation_interface import GithubAuthorisationInterface
from mongo.collection_clients.db_document_client import DbDocumentClient
from mongo.collection_clients.db_github_installation_client import DbGithubInstallationClient
from mongo.collection_clients.db_user_client import DbUserClient
from mongo.models.db_document_model import DbDocumentModel
from mongo.constants.db_fields import DbFields
from tools import logger
from utils.code_formatter import CodeFormatter
from utils.global_constant import GlobalConst

web_server = Blueprint('web_server', __name__)

# TODO: split this file in several files
@web_server.before_request
def before_request_func():
    if request.method == 'OPTIONS':
        return __create_option_response()


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not __is_user_authorised():
            logger.get_logger().info("User not authorised")
            return __create_unauthorised_response()
        return f(*args, **kwargs)

    return wrap


def github_account_login_access_validation_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not __can_user_access_github_account_login():
            return __create_unauthorised_response()
        return f(*args, **kwargs)

    return wrap

@web_server.route("/logout")
@login_required
def logout():
    session.pop('user_login')
    return __create_response({})


@web_server.route("/<path:github_account_login>/repos")
@login_required
@github_account_login_access_validation_required
def repos(github_account_login):
    # Get the repository list

    repo_names = []
    for repo_interface in AuthenticatedGithubInterface(session['user_login']).request_repos(github_account_login):
        repo_names.append({DbFields.NAME_FIELD: repo_interface.repo.name, DbFields.GITHUB_ACCOUNT_LOGIN_FIELD: repo_interface.repo.github_account_login})

    # Return the response
    return __create_response(repo_names)


@web_server.route("/<path:github_account_login>/file")
@login_required
@github_account_login_access_validation_required
def file(github_account_login):
    # Get the repository
    file_github_account_login = request.args.get('file_github_account_login')
    repo_name = request.args.get('repo_name')

    if not repo_name:
        return abort(400, "A repo should be specified")

    repo_interface = AuthenticatedGithubInterface(session['user_login']).request_repo(file_github_account_login, repo_name)

    # Get the content at path
    path_arg = request.args.get('path')
    path = path_arg if path_arg else ""

    # TODO: fix this so we don't have to deepcopy
    fs_node = copy.deepcopy(repo_interface.get_fs_node_at_path(path))

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


@web_server.route("/<path:github_account_login>/save", methods=['POST', 'OPTIONS'])
@login_required
@github_account_login_access_validation_required
def save(github_account_login):
    if DbDocumentClient().find_one(github_account_login, request.get_json().get('name')):
        return abort(400, 'Document name already exists')

    new_doc = request.get_json()
    new_doc[DbFields.GITHUB_ACCOUNT_LOGIN_FIELD] = github_account_login

    DbDocumentClient().insert_one(DbDocumentModel.from_json(new_doc))

    return __create_response({})


@web_server.route("/<path:github_account_login>/docs")
@login_required
@github_account_login_access_validation_required
def docs(github_account_login):
    docs = DbDocumentClient().find(github_account_login)

    return __create_response([doc for doc in docs])


@web_server.route("/<path:github_account_login>/render")
@login_required
@github_account_login_access_validation_required
def render(github_account_login):
    name = request.args.get('name')

    # Get the documentation doc
    doc = DbDocumentClient().find_one(github_account_login, name)

    refs = {}

    for ref in doc.refs:
        repo_interface = AuthenticatedGithubInterface(session['user_login']).request_repo(ref.github_account_login, ref.repo_name)

        lines_from_file_content = repo_interface.get_fs_node_at_path(ref.path).content.splitlines()[ref.start_line - 1: ref.end_line]
        content = '\n'.join(lines_from_file_content)
        formatted_code = CodeFormatter.format(ref.path, content, ref.start_line)
        # TODO: create a function on object sent to the frontend to populate all the non sensitive information that it
        #  contains (to send to the frontend) so that we don't do it manually
        refs[ref.ref_id] = {
            'code': formatted_code,
            'github_account_login': ref.github_account_login,
            'repo': ref.repo_name,
            'path': ref.path,
            'startLine': ref.start_line,
            'endLine': ref.end_line,
        }

    return __create_response({
        'name': name,
        'content': doc.content,
        'refs': refs
    })


# TODO: similar to render -> refactor later
@web_server.route("/<path:github_account_login>/lines")
@login_required
@github_account_login_access_validation_required
def get_lines(github_account_login):
    file_github_account_login = request.args.get('file_github_account_login')
    repo_name = request.args.get('repo_name')
    path = request.args.get('path')
    start_line = int(request.args.get('startLine'))
    end_line = int(request.args.get('endLine'))

    repo_interface = AuthenticatedGithubInterface(session['user_login']).request_repo(file_github_account_login, repo_name)
    content = ''.join(repo_interface.get_fs_node_at_path(path).content.splitlines(keepends=True)[start_line - 1: end_line])

    try:
        lexer = get_lexer_for_filename(path)
    except ClassNotFound:
        lexer = TextLexer()  # use a generic lexer if we can't find anything

    formatter = HtmlFormatter(noclasses=True, linenos='table', linespans='code-line', linenostart=start_line)
    code = highlight(content, lexer, formatter)

    return __create_response({
        'ref_id': str(uuid.uuid1()),  # generate a unique id for the reference
        'code': code,
        'github_account_login': file_github_account_login,
        'repo_name': repo_name,
        'path': path,
        'startLine': start_line,
        'endLine': end_line,
    })


@web_server.route("/auth/github/callback", methods=['POST', 'OPTIONS'])
def auth_github_callback():
    temporary_code = request.args.get('code')
    state = request.args.get('state')

    if state != GlobalConst.SECRET_PASSWORD_FORGERY:
        abort(401)

    user_token = GithubAuthorisationInterface.request_user_token(GlobalConst.CLIENT_ID, GlobalConst.CLIENT_SECRET,
                                                                 temporary_code, GlobalConst.REDIRECT_URL_LOGIN)

    session['user_login'] = GithubAuthorisationInterface.request_user_login(user_token)
    DbUserClient().upsert_user_token(session['user_login'], user_token)

    return __create_response({})


@web_server.route("/installs", methods=['POST', 'OPTIONS'])
@login_required
def installs():
    user_installations = AuthenticatedGithubInterface(session['user_login']).request_installations()

    returned_installations = []
    for installation in user_installations:
        # TODO: delete the use of insert_if_not_exist here if it is now setup using the webhook_endpoints
        DbGithubInstallationClient().insert_if_not_exist(installation.github_account_login, installation.id)
        returned_installations.append(installation)

    return __create_response({
        "installations": returned_installations
    })


@web_server.route("/github_app_installation_callback", methods=['POST', 'OPTIONS'])
@login_required
def github_app_installation_callback():
    installation_id = request.args.get('installation_id')
    setup_action = request.args.get('setup_action')

    installation = {}
    user_installations = AuthenticatedGithubInterface(session['user_login']).request_installations()
    for user_installation in user_installations:
        if int(user_installation.id) == int(installation_id):
            installation = user_installation

    return __create_response({
        DbFields.LOGIN_FIELD: installation.github_account_login
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
        logger.get_logger().info("User not authorised for %s", request.path)
    return authorised


def __can_user_access_github_account_login():
    user_installations = AuthenticatedGithubInterface(session['user_login']).request_installations()
    user = request.path.split('/')[2]

    for installation in user_installations:
        if user == installation.github_account_login:
            return True

    logger.get_logger().info('User %s is not authorised to access this installation for ', user, request.path)
    return False


def __create_unauthorised_response():
    return abort(403)  # Forbidden to access the resource


def __create_response(json):
    return jsonify(json)


def __create_option_response():
    return Response()
