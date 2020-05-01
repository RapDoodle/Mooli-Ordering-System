from flask import Flask

app = Flask(__name__)
app.secret_key = '#&3uy449&GffB0Ug$r7'

@app.route('/', methods = ['GET'])
def index():
    return 'Hello World'

if __name__ == '__main__':
	app.run(port=8000, debug=True)
