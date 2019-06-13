# Oauth

# Context

Oauth allows us to get an authorisation token from a user to act and use the Github API on their resources.

Setup instructions can be found here: https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/  

We have a specific organisation to handle Oauth for us called **CodersDoc**.

https://github.com/organizations/codersdoc/

This allows us to connect repositories to the organisation and make the organisation publish Pull Request comments on
developers PR's.

## Setup Oauth

1. Install ngrok

https://ngrok.com/download

2. Create a tunnel between your localhost and the internet (Ngrok forwards the traffic on a public available URL
to your localhost, as if you had a website online)

```
./ngrok http 5000
```

This will generate a ngrok url of the format `https://c90a6779.ngrok.io/` (there is an http and https endpoint) that will
forward your traffic to `localhost:5000`.

3. Take the generated ngrok url and update with it the **home page url** and **authorisation callback** at the url of
the setting for the organisation (don't forget the trailing `/`, take `https://c90a6779.ngrok.io/` and not 
`https://c90a6779.ngrok.io`)

https://github.com/organizations/codersdoc/settings/applications/1071460

You will also need to update the `NGROK_URL` in the **api/server.py**

4. Run the server by launching in the root folder

```
python api/server.py
```

5. Go to https://YOUR_NGORK_URL/oauth

6. You will be redirected to an authorisation page, press accept and this will give you the oauth authorisation token
that you can use as a regular access token ! You WIN !