from flask import Flask
import utils.logger
from flask_wtf.csrf import CSRFProtect
import utils.config_manager as config

app = Flask(__name__)
app.secret_key = config.get_secret_key()

# Configure CSRF
csrf = CSRFProtect(app)

# Impor admin views
from views.customer_view import customer_view
from views.admin.view_auth import admin_auth
from views.admin.view_dashboard import admin_dashboard
from views.admin.view_category import admin_category
from views.admin.view_order import admin_order
from views.admin.view_product import admin_product
from views.admin.view_redeem_card import admin_redeem_card
from views.admin.view_coupon import admin_coupon
from views.admin.view_staff import admin_staff

app.register_blueprint(customer_view)

# Registe admin views
app.register_blueprint(admin_auth)
app.register_blueprint(admin_dashboard)
app.register_blueprint(admin_category)
app.register_blueprint(admin_order)
app.register_blueprint(admin_product)
app.register_blueprint(admin_redeem_card)
app.register_blueprint(admin_coupon)
app.register_blueprint(admin_staff)

if __name__ == '__main__':
	port = config.get('port')
	debug = config.get('debug')
	if config.get('enable_https'):
		ssl_context = (config.get('cert_path'), config.get('private_key_path'))
		app.run(host = 'mooli.repo.ink', port = port, debug = debug, ssl_context = ssl_context)
	else:
		app.run(host = '0.0.0.0', port = port, debug = debug)
