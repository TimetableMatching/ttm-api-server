from flask_restful import Resource, Api
from flask_restful import reqparse
from extension import mydb
from model import *

db = mydb

class WriteNotice(Resource):
    def post(self):
        ERROR_DICT = {
                "error":"",
                "status":str(0)
            }
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
                    ERROR_DICT['error'] =str(e)
                    return ERROR_DICT

                return {
                    'status':str(1),
                }
                

        except Exception as e:
            ERROR_DICT['error'] =str(e)
            return ERROR_DICT

class DeleteNotice(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('notice_id', type=str)
        args = parser.parse_args()
        ERROR_DICT = {
                "error":"",
                "status":str(0)
            }
        try:
            with db.atomic() as transaction:
                try:
                    NoticeModel.delete().where(NoticeModel.notice_id == args['notice_id']).execute()
                    return {'status':str(1)}
                except Exception as e:
                    transaction.rollback()
                    ERROR_DICT['error'] = str(e)
                    return ERROR_DICT
        except Exception as e:
            ERROR_DICT['error'] =str(e)
            return ERROR_DICT

class UpdateNotice(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('notice_id', type=str)
        parser.add_argument('text', type=str)
        args = parser.parse_args()

        ERROR_DICT = {
                "error":"",
                "status":str(0)
            }
        try:
            with db.atomic() as transaction:
                try:
                    NoticeModel.update(text=args['text']).where(NoticeModel.notice_id == args['notice_id']).execute()
                    return {'status':str(1)}
                except Exception as e:
                    transaction.rollback()
                    return {
                        'status':str(0),
                        'error':str(e),
                    }
        
        except Exception as e:
            ERROR_DICT['error'] =str(e)
            return ERROR_DICT