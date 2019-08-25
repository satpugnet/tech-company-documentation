import hmac
from hashlib import sha1


class SignatureValidator:
    """
    Used to validate the signature of the webhook requests.
    """

    def verify_signature(self, signature, body, github_webhook_secret):
        computed_signature = "sha1=" + hmac.new(str.encode(github_webhook_secret), body, sha1).hexdigest()
        return computed_signature == signature
