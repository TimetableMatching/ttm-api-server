from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse

from service.UserService import CreateUser, DeleteUser, Login
from service.GroupService import CreateGroup

from extension import mydb
from model import *

app = Flask(__name__)
api = Api(app)
db = mydb

api.add_resource(CreateUser, '/add_user')
api.add_resource(Login, '/login')
api.add_resource(CreateGroup, '/add_group')
api.add_resource(DeleteUser, '/del_user')

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        )
    #app.run(debug=True)
