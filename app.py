from flask import Flask
import utils.logger
from flask_wtf.csrf import CSRFProtect
import utils.config_manager as config

app = Flask(__name__)
app.secret_key = config.get_secret_key()

# Configure CSRF
csrf = CSRFProtect(app)

from views.customer_view import customer_view
from views.admin_view import admin_view

app.register_blueprint(customer_view)
app.register_blueprint(admin_view)

if __name__ == '__main__':
	port = config.get('port')
	debug = config.get('debug')
	if config.get('enable_https'):
		ssl_context = (config.get('cert_path'), config.get('private_key_path'))
		app.run(host = 'mooli.repo.ink', port = port, debug = debug, ssl_context = ssl_context)
	else:
		app.run(host = '0.0.0.0', port = port, debug = debug)
