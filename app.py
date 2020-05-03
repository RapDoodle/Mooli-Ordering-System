from flask import Flask
import utils.config_manager as config

app = Flask(__name__)
app.secret_key = config.get_secret_key()

from views.customer_home import customer_home_view

app.register_blueprint(customer_home_view)

if __name__ == '__main__':
	app.run(port=8000, debug=True)
