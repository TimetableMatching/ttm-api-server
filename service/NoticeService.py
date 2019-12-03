from flask_restful import Resource, Api
from flask_restful import reqparse
from extension import mydb
from model import *

db = mydb

class WriteNotice(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('notice', type=str)
            parser.add_argument('team_id', type=str)
            parser.add_argument('author', type=str)
            args = parser.parse_args()

            with db.atomic() as transaction:
                try:
                    NoticeModel\
                        .create(
                            g_id=args['team_id'],
                            text=args['notice'],
                            author=args['author'],
                            created_at =datetime.datetime.now(),
                        )
                except Exception as e:
                    return {
                        'status':str(0),
                        'error':str(e),
                    }

                return {
                    'status':str(1),
                }
                

        except Exception as e:
            return {
                'status':str(0),
                'error':str(e),
            }
