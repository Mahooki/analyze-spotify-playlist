from flask import Flask, request
from service import Service
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'ggg'

@app.route('/api/playlists/me')
@cross_origin()
def playlists():
    auth_token = request.headers.get('spotifyAuthToken')
    myService = Service(auth_token)
    return myService.get_my_playlists().to_json()

if __name__ == '__main__':
    app.run(debug=True)