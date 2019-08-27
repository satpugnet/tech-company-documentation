# TODO: put in env variables (as well as private key)
class SecretConstant:
    """
    Contain all of the secret and sensitive constants used in the backend.
    """

    CLIENT_ID = "Iv1.82c79af55b4c6b95"
    CLIENT_SECRET = "62226729b900229f67ba534a2eb54f74abeadd4b"
    GITHUB_APP_IDENTIFIER = "33713"
    SECRET_PASSWORD_FORGERY = "secret_password"
    REDIRECT_URL_LOGIN = "http://localhost:8080/auth/github/callback"
    GITHUB_WEBHOOK_SECRET = "SatPaulDocumentation"
    FLASK_APP_SECRET_KEY = b'`\xefM\x11\xfd\xef\x1d"\x06\x9ek\xb3r\xb0\xcc\x17\xeb\x85u\xf8$\xc1\x94\xce'
