from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<int:user_id>')
def get_user(user_id):
    return 'User ID: %d' % user_id


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
