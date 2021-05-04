from flask_restful import Resource, Api
from app.api import Password
from app.index import app
from flask_cors import CORS, cross_origin
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api.add_resource(Password, '/api/<password>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)
    #app.run()
