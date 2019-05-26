import json

import requests

"""
https://developer.github.com/v3/repos/hooks/
"""


def get_hooks(oauth_token, owner, repo):
    return requests.get(
        "https://api.github.com/repos/{}/{}/hooks".format(owner, repo),
        headers={'Authorization': 'token {}'.format(oauth_token)}
    ).json()


def subscribe_hooks(oauth_token, owner, repo, url_postback):
    return requests.post(
        "https://api.github.com/repos/{}/{}/hooks".format(owner, repo),
        data=json.dumps({
            "name": "web",
            "active": True,
            "events": [
                "pull_request"
            ],
            "config": {
                "url": url_postback,
                "content_type": "json"
            }
        }),
        headers={'Authorization': 'token {}'.format(oauth_token)}
    ).json()