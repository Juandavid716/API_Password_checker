from flask_restful import Resource, Api
from app.api import Password
from app.index import app
api = Api(app)
api.add_resource(Password, '/api/<password>')

if __name__ == '__main__':
    app.run(debug=True)