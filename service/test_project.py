from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello World2!</h1>'

@app.route('/beepboop')
def beepboop():
    return '<h1>BEEEEEEP!</h1>'

if __name__ == '__main__':
    app.run(debug=True)