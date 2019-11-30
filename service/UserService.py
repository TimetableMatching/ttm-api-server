from flask_restful import Resource, Api
from flask_restful import reqparse
from extension import mydb
from model import *

import hashlib

db = mydb

class CreateUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            parser.add_argument('password', type=str)
            parser.add_argument('name', type=str)
            parser.add_argument('organization', type=str)
            parser.add_argument('schedule', action='append')
            args = parser.parse_args()
            
            ret = {
                'result_message': '',
                'status':str(0),
            }
            with db.atomic() as transaction:
                try:
                    encoded_pw = hashlib\
                        .sha256( str(args['password']).encode()).hexdigest()

                    MemberModel.create(
                        account=str(args['email']),
                        name = str(args['name']),
                        password = encoded_pw,
                        organization = str(args['organization']),
                    )


                except Exception as e:
                    transaction.rollback()
                    ret['result_message']='DB'+str(e)
                    return ret

            with db.atomic() as transaction:
                try:
                    query = MemberModel\
                    .select(MemberModel.id)\
                    .where(MemberModel.account == args['email'])
                    ok = False
                    m_id = 0
                    for ac in query:
                        m_id = ac.id

                    for sc in args['schedule']:
                        TableBlankModel.create(
                            m_id = m_id,
                            day = int(sc[0]),
                            time = int(sc[1]),
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


class DeleteUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()

            with db.atomic() as transaction:
                try:
                    pass
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
                        encoded_pw = hashlib\
                        .sha256( str(args['password']).encode()).hexdigest()
                        if encoded_pw == pw.password:
                            ok=True
                
                except Exception as e:
                    transaction.rollback()
                    return{
                        'error': str(e),
                        'email': args['email'],
                        'status': str(0)
                    }
            if ok:
                #Team
                team_dict = {
                    "Team ID": "",
                    "Team Name", "",
                    "MemberNum", "",    
                }

                #User Info
                user_dict ={
                    "Email": "",
                    "Organization":"",
                    "Name":"",
                    "Schedule": [],
                }

                #Notice Dict
                notice_dict = {
                    "Team_id" : "",
                    "Date":"",
                    "Text":"",
                    "author":"",
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
