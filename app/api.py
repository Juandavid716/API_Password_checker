
from flask_restful import Resource
from app.main import main


class Password(Resource):

    def get_Pass(self,passw):
        password,rank, enumeration  = main(passw)
        return [{'num_it': password , 'range':rank, 'enumeration': enumeration}]

    def get(self, password):
        return self.get_Pass(password)

