import os

from flask import Flask
from flask_paranoid import Paranoid

from server.web_server import web_server
from server.webhook_server import webhook_server
from utils.json.custom_json_encoder import CustomJsonEncoder

app = Flask(__name__)

config = {
    "development": "server.configuration.developement_config.DevelopmentConfig",
    "prod": "server.configuration.prod_config.ProdConfig",
    "default": "server.configuration.developement_config.DevelopmentConfig"
}


config_name = os.getenv('FLASK_CONFIGURATION', 'default')
app.config.from_object(config[config_name])

app.json_encoder = CustomJsonEncoder
app.secret_key = os.urandom(24)

paranoid = Paranoid(app)

app.register_blueprint(webhook_server, url_prefix='/api')
app.register_blueprint(web_server, url_prefix='/api')

if __name__ == '__main__':
    app.run()
