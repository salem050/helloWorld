from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World From Salem Eshete! I am adding my first code change.'


if __name__ == '__main__':
    app.run()
