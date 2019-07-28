from flask import Flask

from server.web_server import web_server
from server.webhook_server import webhook_server
from utils.json.custom_json_encoder import CustomJsonEncoder

app = Flask(__name__)
app.json_encoder = CustomJsonEncoder

app.register_blueprint(webhook_server, url_prefix='/api')
app.register_blueprint(web_server, url_prefix='/api')

if __name__ == '__main__':
    app.run()
