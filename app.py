from flask import Flask

app = Flask(__name__)
app.secret_key = '#&3uy449&GffB0Ug$r7'

from views.customer_home import customer_home_view

app.register_blueprint(customer_home_view)

if __name__ == '__main__':
	app.run(port=8000, debug=True)
