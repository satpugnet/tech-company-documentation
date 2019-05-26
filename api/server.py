from urllib import parse

import requests
from flask import Flask, redirect, request, abort, Response

app = Flask(__name__)


NGROK_URL = "https://47defdd8.ngrok.io/"  # Change this everytime you create a new Ngrok session as url is rotated


@app.route("/oauth")
def oauth():
    return redirect("https://github.com/login/oauth/authorize?" +
                    "client_id=79d39cdf599fedc86256"
                    "&redirect_uri=" + NGROK_URL + "access_token"
                    "&scope=" + parse.quote("repo user")
                    )


@app.route("/access_token")
def access_token():
    # Extract the oauth code
    code = request.args.get('code')

    if not code:
        return Response("No oauth code was returned!", status=400)

    # Request the access token to github
    response = requests.get("https://github.com/login/oauth/access_token?"
                            "client_id=79d39cdf599fedc86256"
                            "&client_secret=77480b2de8821275c61437401ec0e4689ea96d74"
                            "&code=" + code,
                            headers={
                                'Accept': 'application/json'
                            })

    print(response)

    # We get the access token
    access_token = response.json().get("access_token")

    # TODO: store or do whatever we want with the access token here

    return Response("Access token is: " + str(access_token))


if __name__ == '__main__':
    app.run()