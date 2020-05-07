from flask import Flask
import utils.config_manager as config

app = Flask(__name__)
app.secret_key = config.get_secret_key()

from views.customer_home import customer_home_view
from views.admin_view import admin_view

app.register_blueprint(customer_home_view)
app.register_blueprint(admin_view)

if __name__ == '__main__':
	port = config.get('port')
	debug = config.get('debug')
	if config.get('enable_https'):
		ssl_context = (config.get('cert_path'), config.get('private_key_path'))
		print(ssl_context)
		app.run(port = port, debug = debug, ssl_context = ssl_context)
	else:
		app.run(port = port, debug = debug)
