from flask_restful import Resource, Api
from flask_restful import reqparse
from extension import mydb

db = mydb

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
