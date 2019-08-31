import os

from flask import Flask
from flask_paranoid import Paranoid

from tools.json.custom_json_encoder import CustomJsonEncoder
from utils.secret_constant import SecretConstant
from web_server.web_server import web_server
from webhook.webhook_server import webhook_server
from tools import logger

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Initialise Flask
app = Flask(__name__)
DEBUG = app.debug

# Initialise the logger
logger.init(app)
logger.get_logger().info("Flask initialised")

# Add sentry integration
logger.get_logger().info("Initialising Sentry")
sentry_sdk.init(
    dsn=SecretConstant.SENTRY_URL,
    integrations=[FlaskIntegration()],
    environment='dev' if DEBUG else 'prod'
)

# Initialise Flask's configurations
logger.get_logger().info("Initialising the Flask's configurations")
config = {
    "development": "web_server.configuration.development_config.DevelopmentConfig",
    "prod": "web_server.configuration.prod_config.ProdConfig",
    "default": "web_server.configuration.development_config.DevelopmentConfig"
}
config_name = os.getenv('FLASK_CONFIGURATION', 'default')
app.config.from_object(config[config_name])

# Initialise Flask's json encoder
logger.get_logger().info("Initialising the Flask's json encoder")
app.json_encoder = CustomJsonEncoder

# Initialise the Flask's secret key
logger.get_logger().info("Initialising the Flask's secret key")
app.secret_key = SecretConstant.FLASK_APP_SECRET_KEY

# Initialise Paranoid for an extra layer of security
logger.get_logger().info("Initialising Paranoid for an extra layer of security")
paranoid = Paranoid(app)

# Register the web server and the webhook to the Flask app
logger.get_logger().info("Registing the web server and the webhook to the Flask app")

app.register_blueprint(webhook_server, url_prefix='/api')
app.register_blueprint(web_server, url_prefix='/api')

# Run the app
logger.get_logger().info("Running the app")


if __name__ == '__main__':
    app.run()
