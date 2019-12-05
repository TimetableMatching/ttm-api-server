
from flask_restful import Resource, Api
from flask_restful import reqparse
from extension import mydb
from model import *

db = mydb

class AddTimeTable(Resource):
    def post(self):
        ERROR_DICT = {
                "error":"",
                "status":str(0)
            }
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            parser.add_argument('schedule', action='append')
            args = parser.parse_args()
            
            with db.atomic() as transaction:
                member_id = 0
                try:
                    # m_id get
                    subq = MemberModel.select(MemberModel.id).where(MemberModel.account==args['email']).dicts()
                    for row in subq:
                        member_id = row['id']

                    for sch in args['schedule']:
                        TableBlankModel.create(
                            mem_id=member_id,
                            day=sch[0],
                            time=sch[1],
                        )

                    return{'status' : str(1)}

                except Exception as e:
                    transaction.rollback()
                    ERROR_DICT['error']=str(e)
                    return ERROR_DICT

        except Exception as e:
            ERROR_DICT['error']=str(e)
            return ERROR_DICT


class ChangeTimeTable(Resource):
    def post(self):
        ERROR_DICT = {
                "error":"",
                "status":str(0)
            }
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            args = parser.parse_args()
            # DB에서 E-mail이 args['email']인 사람을 찾아서, id(숫자)를 가져온 다음
            # 그 id에 해당하는 시간표를 모두 삭제하고
            # args['schedule']에 주어진 시간표로 다시 등록하세요.
            # 시간표 형식은 "(요일)(시간)"입니다. "21"이라면 day=2, time=1 입니다.
            # db 모델은 model.py에서 참고해주세요.
            with db.atomic() as transaction:
                member_id = 0
                try:
                    subq = MemberModel.select(MemberModel.id).where(MemberModel.account==args['email']).dicts()

                    for row in subq:
                        member_id = row['id']
                        TableBlankModel.delete().where(TableBlankModel.m_id == row['id']).execute()

                    return{"status":str(1)}


                except Exception as e:
                    transaction.rollback()
                    ERROR_DICT['error']=str(e)
                    return ERROR_DICT


        except Exception as e:
            ERROR_DICT['error']=str(e)
            return ERROR_DICT
