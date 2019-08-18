import hmac
from hashlib import sha1


class SignatureValidator:
    def verify_signature(self, signature, body, github_webhook_secret):
        computed_signature = "sha1=" + hmac.new(str.encode(github_webhook_secret), body, sha1).hexdigest()
        return computed_signature == signature
