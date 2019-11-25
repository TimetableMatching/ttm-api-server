from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse

from extension import mydb
from model import *

app = Flask(__name__)
api = Api(app)
db = mydb

class CreateUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            parser.add_argument('password', type=str)
            parser.add_argument('name', type=str)
            parser.add_argument('organization', type=str)
            args = parser.parse_args()

            ret = {
                'result_message': '',
                'status':str(0),
            }

            with db.atomic() as transaction:
                try:
                    MemberModel.create(
                        account=str(args['email']),
                        name = str(args['name']),
                        password = str(args['password']),
                        organization = str(args['organization']),
                    )
                except Exception as e:
                    transaction.rollback()
                    ret['result_message']='DB'+str(e)
                    return ret

            ret['status']=str(1)
            ret['email']=args['email']
            ret['result_message']='success'

            return ret
        except Exception as e:
            return {'error': str(e), 'status':str(0)}


class Login(Resource):
    def post(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('email',type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()

            with db.atomic() as transaction:
                try:
                    query = MemberModel\
                    .select(MemberModel.password)\
                    .where(MemberModel.account == args['email'])

                    ok = False
                    for pw in query:
                        print(pw.password)
                        if args['password'] == pw.password:
                            ok=True
                
                except Exception as e:
                    transaction.rollback()
                    return{
                        'error': str(e),
                        'email': args['email'],
                        'status': str(0)
                    }
            if ok:
                return{
                    'email': args['email'],
                    'status': str(1)
                }
            else:
                return{
                    'email': args['email'],
                    'status': str(0)
                }

        except Exception as e:
            return{
                        'error': str(e),
                        'email': args['email'],
                        'status': str(0)
                    }


class CreateGroup(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            args = parser.parse_args()

            with db.atomic() as transaction:
                try:
                    GroupModel.create(
                        name = str(args['name']),
                    )
                except Exception as e:
                    transaction.rollback()
                    return{
                        'result_message': 'DB:'+str(e),
                        'status' : str(0)
                    }

            return {
                'name': args['name'],
                'status': str(1),
                'result_message': 'success',
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': str(0)
                }

class DeleteUser(Resource):
    def post(def):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            parser.add_argument('password' type=str)
            args = parser.parse_args()

            with db.atomic() as transaction:
                try:

                    ## Fill Code Here
                    
                except Exception as e:
                    transaction.rollback()
                    return{
                        'result_message': 'DB:'+str(e),
                        'status' : str(0)
                    }

            return {
                'name': args['email'],
                'status': str(1),
                'result_message': 'succeed to delete user '+args['email'],
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': str(0)
                }


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
